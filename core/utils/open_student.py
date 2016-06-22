from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Max

from core.models import Submission, School, ClassRoom, SubjectRoom, AssignmentQuestionsList
from core.utils.assignment import is_corrected_open_assignment
from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup, HWCentralOpen, HWCentralRepo


# TODO: reduce query duplication

def calculate_open_aql_average(aql):
    """
    Returns None if no data
    """

    # find all open students that have submitted corrected assignments for the same aql
    students = Submission.objects.filter(
        student__userinfo__group=HWCentralGroup.refs.OPEN_STUDENT,
        assignment__content_type=ContentType.objects.get_for_model(User),
        assignment__assignmentQuestionsList=aql,
        marks__isnull=False
    ).values_list('student', flat=True).distinct()

    if len(students) == 0:
        return None

    total = 0
    for student_pk in students:
        # for every student, get the max marks across all submissions
        total += Submission.objects.filter(
            student__pk=student_pk,
            assignment__content_type=ContentType.objects.get_for_model(User),
            assignment__object_id=student_pk,
            assignment__assignmentQuestionsList=aql,
            marks__isnull=False
        ).aggregate(Max('marks'))['marks__max']

    return float(total) / len(students)


def get_adjacent_open_submissions(assignment):
    assert is_corrected_open_assignment(assignment)

    aql = assignment.assignmentQuestionsList
    # find all open students that have submitted corrected assignments for the same aql
    students = Submission.objects.filter(
        student__userinfo__group=HWCentralGroup.refs.OPEN_STUDENT,
        assignment__content_type=ContentType.objects.get_for_model(User),
        assignment__assignmentQuestionsList=aql,
        marks__isnull=False
    ).values_list('student', flat=True).distinct()

    assert len(students) > 0

    submissions = []
    for student_pk in students:
        # for every student, get the submission with the max mark
        submissions.append(Submission.objects.filter(
            student__pk=student_pk,
            assignment__content_type=ContentType.objects.get_for_model(User),
            assignment__object_id=student_pk,
            assignment__assignmentQuestionsList=aql,
            marks__isnull=False
        ).order_by('-marks')[0])

    return submissions


class OpenStudentUtils(UserUtils):
    def __init__(self, open_student):
        assert open_student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT
        self.UTILS_GROUP = HWCentralGroup.refs.OPEN_STUDENT
        super(OpenStudentUtils, self).__init__(open_student)

    def get_num_unfinished_assignments(self):
        # check for any student assignments that have not been submitted for correction
        return self.get_uncorrected().count()

    def get_announcements_query(self):
        school_type = ContentType.objects.get_for_model(School)
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        user_type = ContentType.objects.get_for_model(User)

        target_condition = (
            Q(content_type=school_type, object_id=HWCentralOpen.refs.SCHOOL.pk) |
            Q(content_type=classroom_type, object_id=HWCentralOpen.refs.CLASSROOM.pk) |
            Q(content_type=subjectroom_type,
              object_id__in=HWCentralOpen.refs.SUBJECTROOMS.values_list('pk', flat=True)) |
            Q(content_type=user_type, object_id=self.user.pk)
        )

        return (target_condition & OpenStudentUtils.RECENT_ANNOUNCEMENT_CONDITION)

    def get_corrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         marks__isnull=False
                                         ).order_by('-assignment__due')

    def get_uncorrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         marks__isnull=True
                                         ).order_by('-assignment__due')

    def get_attempted_aqls(self, subjectroom):
        # find all question sets for this subjectroom which user has attempted
        return Submission.objects.filter(
            student=self.user,
            assignment__content_type=ContentType.objects.get_for_model(User),
            assignment__object_id=self.user.pk,
            assignment__assignmentQuestionsList__subject=subjectroom.subject,
            marks__isnull=False
        ).values_list('assignment__assignmentQuestionsList', flat=True).distinct()

    def get_subjectroom_average(self, subjectroom):
        """
        This needs to have access to user object since the subjectroom average is calculated by selecting only those aqls the user has attempted

        Returns None if no data
        """
        assert subjectroom.classRoom == HWCentralOpen.refs.CLASSROOM
        # find all question sets for this subjectroom which user has attempted
        aqls = self.get_attempted_aqls(subjectroom)

        total_aqls = len(aqls)

        if total_aqls == 0:
            return None

        net_score = 0

        for aql_pk in aqls:
            # HACK: Not true average as instead of taking mean of highest marks for every aql across every user we take highest mark for every aql across all users
            submission_query = Submission.objects.filter(
                student__userinfo__group=HWCentralGroup.refs.OPEN_STUDENT,
                assignment__content_type=ContentType.objects.get_for_model(User),
                assignment__assignmentQuestionsList__pk=aql_pk,
                marks__isnull=False
            )
            assert submission_query.count() > 0
            net_score += submission_query.aggregate(Max('marks'))['marks__max']

        return float(net_score) / total_aqls

    def get_average(self, subjectroom):
        """
        Returns None if no data
        """
        assert subjectroom.classRoom == HWCentralOpen.refs.CLASSROOM
        # find all question sets for this subjectroom which user has attempted
        aqls = self.get_attempted_aqls(subjectroom)

        total_aqls = len(aqls)

        if total_aqls == 0:
            return None

        net_score = 0

        for aql_pk in aqls:
            submission_query = Submission.objects.filter(
                student=self.user,
                assignment__content_type=ContentType.objects.get_for_model(User),
                assignment__object_id=self.user.pk,
                assignment__assignmentQuestionsList__pk=aql_pk,
                marks__isnull=False
            )
            assert submission_query.count() > 0
            net_score += submission_query.aggregate(Max('marks'))['marks__max']

        return float(net_score) / total_aqls

    def get_cumulative(self, subjectroom, metric):

        # find all question sets for this subjectroom
        aqls = AssignmentQuestionsList.objects.filter(school=HWCentralRepo.refs.SCHOOL,
                                                      subject=subjectroom.subject)
        # find the best score by this user in each of those question sets
        total_progress = 0
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
                total_progress += submission_query.aggregate(Max(metric))[metric + '__max']

        progress = float(total_progress) / total_aqls
        # give starting visibility to progress
        if (progress > 0) and (progress < 0.005):
            progress += 0.005
        return progress

    def get_completion(self, subjectroom):

        assert subjectroom.classRoom == HWCentralOpen.refs.CLASSROOM

        return self.get_cumulative(subjectroom, 'completion')

    def get_proficiency(self, subjectroom):

        assert subjectroom.classRoom == HWCentralOpen.refs.CLASSROOM

        return self.get_cumulative(subjectroom, 'marks')


class OpenStudentSubjectIdUtils(OpenStudentUtils):
    def __init__(self, student, subjectroom):
        super(OpenStudentSubjectIdUtils, self).__init__(student)
        self.subjectroom = subjectroom
        assert subjectroom.classRoom == HWCentralOpen.refs.CLASSROOM

    def get_corrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         assignment__assignmentQuestionsList__subject=self.subjectroom.subject,
                                         marks__isnull=False
                                         ).order_by('-assignment__due')

    def get_uncorrected(self):
        return Submission.objects.filter(student=self.user,
                                         assignment__content_type=ContentType.objects.get_for_model(User),
                                         assignment__object_id=self.user.pk,
                                         assignment__assignmentQuestionsList__subject=self.subjectroom.subject,
                                         marks__isnull=True
                                         ).order_by('-assignment__due')
