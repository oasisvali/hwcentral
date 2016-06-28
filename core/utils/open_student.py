from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Max, Avg, Sum

from core.models import Submission, School, ClassRoom, SubjectRoom, AssignmentQuestionsList, OpenStudentHighest
from core.utils.assignment import is_corrected_open_assignment
from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup, HWCentralOpen, HWCentralRepo


# TODO: reduce query duplication

def calculate_open_aql_average(aql):
    """
    Returns None if no data
    """

    # find all highest scores for this aql
    scores = OpenStudentHighest.objects.filter(submission__assignment__assignmentQuestionsList=aql)
    if scores.count() == 0:
        return None

    # get average of highest score for every user
    return scores.aggregate(Avg('submission__marks'))['submission__marks__avg']


def get_adjacent_open_submissions(assignment):
    assert is_corrected_open_assignment(assignment)

    aql = assignment.assignmentQuestionsList
    # find all highest scores for this aql
    scores = OpenStudentHighest.objects.filter(submission__assignment__assignmentQuestionsList=aql)

    assert scores.count() > 0

    return [highest.submission for highest in scores]


class OpenStudentUtils(UserUtils):
    def __init__(self, open_student):
        assert open_student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT
        self.UTILS_GROUP = HWCentralGroup.refs.OPEN_STUDENT
        super(OpenStudentUtils, self).__init__(open_student)
        self.standard = (self.user.classes_enrolled_set.get()).standard

    def get_num_unfinished_assignments(self):
        # check for any student assignments that have not been submitted for correction
        return self.get_uncorrected().count()

    def get_announcements_query(self):
        school_type = ContentType.objects.get_for_model(School)
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        user_type = ContentType.objects.get_for_model(User)
        student_subjectroom_ids = self.user.subjects_enrolled_set.values_list('pk', flat=True)

        target_condition = (
            Q(content_type=school_type, object_id=HWCentralOpen.refs.SCHOOL.pk) |
            Q(content_type=classroom_type, object_id=(self.user.classes_enrolled_set.get()).pk) |
            Q(content_type=subjectroom_type,
              object_id__in=student_subjectroom_ids) |
            Q(content_type=user_type, object_id=self.user.pk)
        )

        return (target_condition & OpenStudentUtils.RECENT_ANNOUNCEMENT_CONDITION)

    def get_corrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         marks__isnull=False,
                                         assignment__assignmentQuestionsList__standard=self.standard
                                         ).order_by('-assignment__due')

    def get_uncorrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         marks__isnull=True,
                                         assignment__assignmentQuestionsList__standard=self.standard
                                         ).order_by('-assignment__due')

    def get_subjectroom_scores(self, subjectroom):
        # find all scores for this user in the given subjectroom
        return OpenStudentHighest.objects.filter(student=self.user,
                                                 submission__assignment__assignmentQuestionsList__subject=subjectroom.subject,
                                                 submission__assignment__assignmentQuestionsList__standard=subjectroom.classRoom.standard)

    def get_subjectroom_average(self, subjectroom):
        """
        This needs to have access to user object since the subjectroom average is calculated by selecting only those aqls the user has attempted

        Returns None if no data
        """
        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL
        assert subjectroom.classRoom == self.user.classes_enrolled_set.get()
        # find all question sets for this subjectroom which user has attempted
        aqls = self.get_subjectroom_scores(subjectroom).values_list('submission__assignment__assignmentQuestionsList',
                                                                    flat=True)

        total_aqls = len(aqls)

        if total_aqls == 0:
            return None

        net_score = 0

        for aql_pk in aqls:
            scores = OpenStudentHighest.objects.filter(submission__assignment__assignmentQuestionsList__pk=aql_pk)
            assert scores.count() > 0  # at least the current user has a score for this aql
            net_score += scores.aggregate(Avg('submission__marks'))['submission__marks__avg']

        return float(net_score) / total_aqls

    def get_average(self, subjectroom):
        """
        Returns None if no data
        """
        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL
        assert subjectroom.classRoom == self.user.classes_enrolled_set.get()

        # find all question sets for this subjectroom which user has attempted
        scores = self.get_subjectroom_scores(subjectroom)

        if scores.count() == 0:
            return None

        return scores.aggregate(Avg('submission__marks'))['submission__marks__avg']

    def get_completion(self, subjectroom):

        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL
        assert subjectroom.classRoom == self.user.classes_enrolled_set.get()

        # find all question sets for this subjectroom
        aqls = get_aqls_for_open_subjectroom(subjectroom)
        # find the best score by this user in each of those question sets
        total_completion = 0
        total_aqls = aqls.count()

        if total_aqls == 0:
            return 0

        for aql in aqls:
            submission_query = Submission.objects.filter(
                student=self.user,
                assignment__content_type=ContentType.objects.get_for_model(User),
                assignment__object_id=self.user.pk,
                assignment__assignmentQuestionsList=aql,
                marks__isnull=False
            )

            if submission_query.count() > 0:
                total_completion += submission_query.aggregate(Max('completion'))['completion__max']

        completion = float(total_completion) / total_aqls
        return give_starting_boost(completion)

    def get_proficiency(self, subjectroom):

        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL
        assert subjectroom.classRoom == self.user.classes_enrolled_set.get()

        # find all question sets for this subjectroom
        aqls = get_aqls_for_open_subjectroom(subjectroom).values_list('pk', flat=True)

        # find the best score by this user in each of those question sets
        total_proficiency = 0
        total_aqls = len(aqls)

        if total_aqls == 0:
            return 0

        scores = OpenStudentHighest.objects.filter(submission__assignment__assignmentQuestionsList__pk__in=aqls,
                                                   student=self.user)
        if scores.count() > 0:
            total_proficiency = scores.aggregate(Sum('submission__marks'))['submission__marks__sum']

        proficiency = float(total_proficiency) / total_aqls
        return give_starting_boost(proficiency)


def give_starting_boost(metric):
    if (metric > 0) and (metric < 0.005):
        metric += 0.005
    return metric


def get_aqls_for_open_subjectroom(subjectroom):
    return AssignmentQuestionsList.objects.filter(school=HWCentralRepo.refs.SCHOOL,
                                                  subject=subjectroom.subject,
                                                  standard=subjectroom.classRoom.standard)

class OpenStudentSubjectIdUtils(OpenStudentUtils):
    def __init__(self, student, subjectroom):
        super(OpenStudentSubjectIdUtils, self).__init__(student)
        self.subjectroom = subjectroom
        self.standard = subjectroom.classRoom.standard
        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL
        assert subjectroom.classRoom == self.user.classes_enrolled_set.get()

    def get_corrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         assignment__assignmentQuestionsList__subject=self.subjectroom.subject,
                                         assignment__assignmentQuestionsList__standard=self.standard,
                                         marks__isnull=False
                                         ).order_by('-assignment__due')

    def get_uncorrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         assignment__assignmentQuestionsList__subject=self.subjectroom.subject,
                                         assignment__assignmentQuestionsList__standard=self.standard,
                                         marks__isnull=True
                                         ).order_by('-assignment__due')
