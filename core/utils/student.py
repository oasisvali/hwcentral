import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.models import Assignment, Submission, Announcement, School, ClassRoom, SubjectRoom







# Constants for limiting data returned
from core.utils.references import HWCentralGroup

MAX_UNFINISHED_ASSIGNMENTS = 10
MAX_GRADED_SUBMISSIONS = 10
MAX_ANNOUNCEMENTS = 10


class StudentUtils(object):
    def __init__(self, student):
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT
        self.student = student

    def get_num_unfinished_assignments(self):
        # check if 100% submissions have been posted for each assignment
        num_unfinished_assignments = 0
        for assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(assignment=assignment, student=self.student)
                if submission.completion < 1:
                    num_unfinished_assignments += 1
            except Submission.DoesNotExist:
                num_unfinished_assignments += 1

        return num_unfinished_assignments

    def get_enrolled_subjectroom_ids(self):
        return self.student.subjects_enrolled_set.values_list('pk', flat=True)

    def get_active_assignments(self):
        now = django.utils.timezone.now()
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()

        return Assignment.objects.filter(subjectRoom__pk__in=student_subjectroom_ids, due__gte=now,
                                         assigned__lte=now).order_by('-due')

    def get_announcements(self):
        school_type = ContentType.objects.get_for_model(School)
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()

        query = (Q(content_type=school_type, object_id=self.student.userinfo.school.pk) |
                 Q(content_type=classroom_type, object_id=self.student.classes_enrolled_set.get().pk) |
                 Q(content_type=subjectroom_type, object_id__in=student_subjectroom_ids))

        return Announcement.objects.filter(query).order_by('-timestamp')

    def get_active_assignments_with_completion(self):
        result = []
        for active_assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(student=self.student, assignment=active_assignment)
                completion = submission.completion
            except Submission.DoesNotExist:
                completion = 0.0
            result.append((active_assignment, completion))
        return result

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.student, assignment__due__lte=now).order_by('-assignment__due')


class StudentSubjectIdUtils(StudentUtils):
    def __init__(self, student, subjectroom):
        super(StudentSubjectIdUtils, self).__init__(student)
        self.subjectroom = subjectroom

    def get_active_assignments(self):
        now = django.utils.timezone.now()

        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__gte=now,
                                         assigned__lte=now).order_by('-due')

    def get_announcements(self):
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)

        return Announcement.objects.filter(content_type=subjectroom_type, object_id=self.subjectroom.pk).order_by(
            '-timestamp')

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.student, assignment__subjectRoom=self.subjectroom,
                                         assignment__due__lte=now).order_by('-assignment__due')
