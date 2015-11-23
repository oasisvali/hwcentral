import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum, Avg

from core.models import Announcement, School, ClassRoom, SubjectRoom, Assignment, Submission
from core.utils.assignment import is_assignment_active
from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup


class TeacherAdminSharedUtils(UserUtils):
    """
    ABSTRACT USAGE ONLY - all common logic between teacher and admin to live here
    """

    def get_announcements_query(self):
        school_type = ContentType.objects.get_for_model(School)
        subjectroom_ids = self.get_managed_subjectroom_ids()
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        classroom_ids = self.get_managed_classroom_ids()
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        target_condition = (Q(content_type=classroom_type, object_id__in=classroom_ids)
                 | Q(content_type=school_type, object_id=self.user.userinfo.school.pk)
                 | Q(content_type=subjectroom_type, object_id__in=subjectroom_ids))

        return (target_condition & TeacherAdminSharedUtils.RECENT_ANNOUNCEMENT_CONDITION)

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
        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__lte=now).order_by('-due')[:TeacherAdminSharedUtils.CORRECTED_ASSIGNMENTS_LIMIT]

    def get_managed_classroom_ids(self):
        raise NotImplementedError("subclass of TeacherAdminSharedUtils must implement method get_managed_classroom_ids")

    def get_managed_subjectroom_ids(self):
        raise NotImplementedError(
            "subclass of TeacherAdminSharedUtils must implement method get_managed_subjectroom_ids")

class TeacherAdminSharedSubjectIdUtils(TeacherAdminSharedUtils):
    """
    ABSTRACT USAGE ONLY
    """
    def __init__(self, user, subjectroom):
        super(TeacherAdminSharedSubjectIdUtils, self).__init__(user)
        self.subjectroom = subjectroom

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__gte=now).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__lte=now).order_by('-due')[:TeacherAdminSharedUtils.CORRECTED_ASSIGNMENTS_LIMIT]

    def get_subjectroom_reportcard_info(self):
        result = []
        students = self.subjectroom.students.all()
        now = django.utils.timezone.now()
        for student in students:
            average = Submission.objects.filter(student=student, assignment__subjectRoom=self.subjectroom,
                                                assignment__due__lte=now).aggregate(Avg("marks"))['marks__avg']
            result.append((student, average))
        return result

    def get_subjectroom_average(self):
        return self.get_corrected_assignments().aggregate(Avg('average'))['average__avg']

## The following classes are for external use (because they contain user group checks)

class TeacherGroupUtils(object):
    """
    mixin to enable teacher user group checking
    """
    UTILS_GROUP = HWCentralGroup.refs.TEACHER

class TeacherUtils(TeacherGroupUtils, TeacherAdminSharedUtils):
    def get_managed_classroom_ids(self):
        return self.user.classes_managed_set.values_list('pk', flat=True)

    def get_managed_subjectroom_ids(self):
        return self.user.subjects_managed_set.values_list('pk', flat=True)

class TeacherSubjectIdUtils(TeacherGroupUtils, TeacherAdminSharedSubjectIdUtils):
    pass

class ClassroomIdUtils(object):
    def __init__(self, classroom):
        self.classroom = classroom

    def get_contained_subjectrooms(self):
        return SubjectRoom.objects.filter(classRoom=self.classroom).order_by('subject__name')

    def get_contained_subjectroom_ids(self):
        return self.get_contained_subjectrooms().values_list('pk', flat=True)

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_contained_subjectroom_ids()

        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__gte=now).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_contained_subjectroom_ids()
        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__lte=now).order_by('-due')[:UserUtils.CORRECTED_ASSIGNMENTS_LIMIT]

    def get_reportcard_row_info(self):
        results = []
        now = django.utils.timezone.now()
        for student in self.classroom.students.all():
            averages = []
            for subjectroom in self.get_contained_subjectrooms():
                averages.append(Submission.objects.filter(student=student, assignment__subjectRoom=subjectroom,
                                                          assignment__due__lte=now).aggregate(Avg('marks'))[
                                    'marks__avg'])

            # dont really need the classroom check below but what the heck why not
            aggregate = Submission.objects.filter(student=student, assignment__due__lte=now,
                                                  assignment__subjectRoom__classRoom=self.classroom).aggregate(
                Avg('marks'))['marks__avg']
            results.append((student, averages, aggregate))

        return results

    def get_classroom_averages_by_subject(self):
        results = []
        now = django.utils.timezone.now()
        for subjectroom in self.get_contained_subjectrooms():
            results.append(Assignment.objects.filter(subjectRoom=subjectroom, due__lte=now).aggregate(Avg('average'))[
                               'average__avg'])

        return results

    def get_classroom_average(self):
        return self.get_corrected_assignments().aggregate(Avg('average'))['average__avg']