import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum

from core.models import Announcement, School, ClassRoom, SubjectRoom, Assignment, Submission
from core.utils.assignment import is_assignment_active
from core.utils.references import HWCentralGroup


class TeacherAdminSharedUtils(object):
    """
    ABSTRACT USAGE ONLY
    """

    def __init__(self, user):
        self.user = user

    def get_announcements(self):
        school_type = ContentType.objects.get_for_model(School)
        subjectroom_ids = self.get_managed_subjectroom_ids()
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        classroom_ids = self.get_managed_classroom_ids()
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        query = (Q(content_type=classroom_type, object_id__in=classroom_ids)
                 | Q(content_type=school_type, object_id=self.user.userinfo.school.pk)
                 | Q(content_type=subjectroom_type, object_id__in=subjectroom_ids))

        return Announcement.objects.filter(query).order_by('-timestamp')

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_managed_subjectroom_ids()

        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__gte=now).order_by('-due')

    def get_uncorrected_assignments_with_info(self):
        results = []
        for uncorrected_assignment in self.get_uncorrected_assignments():
            if not is_assignment_active(uncorrected_assignment):
                # inactive assignment must have 0 submissions_received
                results.append((uncorrected_assignment,
                                False,
                                0))
                continue

            completion_sum = Submission.objects.filter(assignment=uncorrected_assignment).aggregate(Sum('completion'))[
                'completion__sum']
            if completion_sum is None:  # active assignment but no submissions yet
                completion_avg = 0
            else:
                completion_avg = float(completion_sum) / uncorrected_assignment.subjectRoom.students.count()

            results.append((uncorrected_assignment,
                            True,
                            completion_avg))

        return results

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_managed_subjectroom_ids()
        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__lte=now).order_by('-due')

    def get_managed_classroom_ids(self):
        raise NotImplementedError("subclass of TeacherAdminSharedUtils must implement method get_managed_classroom_ids")

    def get_managed_subjectroom_ids(self):
        raise NotImplementedError(
            "subclass of TeacherAdminSharedUtils must implement method get_managed_subjectroom_ids")


class TeacherUtils(TeacherAdminSharedUtils):
    def __init__(self, teacher):
        assert teacher.userinfo.group == HWCentralGroup.refs.TEACHER
        super(TeacherUtils, self).__init__(teacher)

    def get_managed_classroom_ids(self):
        return self.user.classes_managed_set.values_list('pk', flat=True)

    def get_managed_subjectroom_ids(self):
        return self.user.subjects_managed_set.values_list('pk', flat=True)


class TeacherAdminSharedSubjectIdUtils(TeacherAdminSharedUtils):
    def __init__(self, user, subjectroom):
        super(TeacherAdminSharedSubjectIdUtils, self).__init__(user)
        self.subjectroom = subjectroom

    def get_announcements(self):
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        return Announcement.objects.filter(content_type=subjectroom_type, object_id=self.subjectroom.pk).order_by(
            '-timestamp')

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__gte=now).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__lte=now).order_by('-due')


class TeacherSubjectIdUtils(TeacherAdminSharedSubjectIdUtils):
    def __init__(self, teacher, subjectroom):
        assert teacher.userinfo.group == HWCentralGroup.refs.TEACHER
        super(TeacherSubjectIdUtils, self).__init__(teacher, subjectroom)


class AdminSubjectIdUtils(TeacherAdminSharedSubjectIdUtils):
    def __init__(self, admin, subjectroom):
        assert admin.userinfo.group == HWCentralGroup.refs.ADMIN
        super(AdminSubjectIdUtils, self).__init__(admin, subjectroom)
