import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.models import Assignment, Submission, School, ClassRoom, SubjectRoom
from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup


class StudentUtils(UserUtils):
    def __init__(self, student):
        self.UTILS_GROUP = HWCentralGroup.refs.STUDENT
        super(StudentUtils, self).__init__(student)

    def get_num_unfinished_assignments(self):
        # check if 100% submissions have been posted for each assignment
        num_unfinished_assignments = 0
        for assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(assignment=assignment, student=self.user)
                if submission.completion < 1:
                    num_unfinished_assignments += 1
            except Submission.DoesNotExist:
                num_unfinished_assignments += 1

        return num_unfinished_assignments

    def get_enrolled_subjectroom_ids(self):
        return self.user.subjects_enrolled_set.values_list('pk', flat=True)

    def get_enrolled_remedial_ids(self):
        return self.user.remedials_enrolled_set.values_list('pk', flat=True)

    def get_active_assignments(self):
        now = django.utils.timezone.now()
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()
        student_remedial_ids = self.get_enrolled_remedial_ids()

        return Assignment.objects.filter(
                (Q(subjectRoom__pk__in=student_subjectroom_ids) | Q(remedial__pk__in=student_remedial_ids))
                & Q(due__gte=now) & Q(assigned__lte=now)
        ).order_by('-due')

    def get_announcements_query(self):
        school_type = ContentType.objects.get_for_model(School)
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()

        target_condition = (Q(content_type=school_type, object_id=self.user.userinfo.school.pk) |
                 Q(content_type=classroom_type, object_id=self.user.classes_enrolled_set.get().pk) |
                 Q(content_type=subjectroom_type, object_id__in=student_subjectroom_ids))

        return (target_condition & StudentUtils.RECENT_ANNOUNCEMENT_CONDITION)


    def get_active_assignments_with_completion(self):
        result = []
        for active_assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(student=self.user, assignment=active_assignment)
                completion = submission.completion
            except Submission.DoesNotExist:
                completion = 0.0
            result.append((active_assignment, completion))
        return result

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.user, assignment__due__lte=now).order_by('-assignment__due')


class StudentSubjectIdUtils(StudentUtils):
    def __init__(self, student, subjectroom):
        super(StudentSubjectIdUtils, self).__init__(student)
        self.subjectroom = subjectroom

    def get_active_assignments(self):
        now = django.utils.timezone.now()

        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__gte=now,
                                         assigned__lte=now).order_by('-due')

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.user, assignment__subjectRoom=self.subjectroom,
                                         assignment__due__lte=now).order_by('-assignment__due')


class StudentFocusIdUtils(StudentUtils):
    def __init__(self, student, focusroom):
        super(StudentFocusIdUtils, self).__init__(student)
        self.focusroom = focusroom

    def get_active_assignments(self):
        now = django.utils.timezone.now()

        active_assignments = []
        for assignment in Assignment.objects.filter(remedial__focusRoom=self.focusroom, due__gte=now,
                                                    assigned__lte=now).order_by('-due'):
            if self.user in assignment.content_object.students.all():
                active_assignments.append(assignment)

        return active_assignments

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.user, assignment__remedial__focusRoom=self.focusroom,
                                         assignment__due__lte=now).order_by('-assignment__due')
