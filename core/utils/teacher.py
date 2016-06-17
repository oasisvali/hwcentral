import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum, Avg

from core.models import School, ClassRoom, SubjectRoom, Assignment, Submission
from core.utils.assignment import is_assignment_active, is_assignment_corrected
from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup
from focus.models import FocusRoom


class UncorrectedAssignmentInfoMixin(object):
    def get_uncorrected_assignments(self):
        raise NotImplementedError(
            "Class using UncorrectedAssignmentInfoMixin must implement get_uncorrected_assignments")

    def get_uncorrected_assignments_with_info(self):
        results = []
        for uncorrected_assignment in self.get_uncorrected_assignments():
            assignment_active, completion_avg = get_uncorrected_assignment_completion_avg(uncorrected_assignment)
            results.append((uncorrected_assignment,
                            assignment_active,
                            completion_avg))

        return results


def get_uncorrected_assignment_completion_avg(assignment):
    assert not is_assignment_corrected(assignment)
    if not is_assignment_active(assignment):
        return (False, 0)  # inactive assignment must have 0 submission
    assignment_active = True
    completion_sum = Submission.objects.filter(assignment=assignment).aggregate(Sum('completion'))[
        'completion__sum']
    if completion_sum is None:  # no submissions yet
        return (assignment_active, 0)
    else:
        return (assignment_active, float(completion_sum) / assignment.content_object.students.count())

class TeacherAdminSharedUtils(UncorrectedAssignmentInfoMixin, UserUtils):
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

        filter = Q(subjectRoom__pk__in=self.get_managed_subjectroom_ids())
        if self.focus:
            filter |= Q(remedial__focusRoom__pk__in=self.get_managed_focusroom_ids())

        return Assignment.objects.filter(filter & Q(due__gte=now)).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()

        filter = Q(subjectRoom__pk__in=self.get_managed_subjectroom_ids())
        if self.focus:
            filter |= Q(remedial__focusRoom__pk__in=self.get_managed_focusroom_ids())

        return Assignment.objects.filter(filter & Q(due__lte=now)).order_by('-due')

    def get_managed_classroom_ids(self):
        raise NotImplementedError("subclass of TeacherAdminSharedUtils must implement method get_managed_classroom_ids")

    def get_managed_subjectroom_ids(self):
        raise NotImplementedError(
            "subclass of TeacherAdminSharedUtils must implement method get_managed_subjectroom_ids")

    def get_managed_focusroom_ids(self):
        raise NotImplementedError(
                "subclass of TeacherAdminSharedUtils must implement method get_managed_focusroom_ids")

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
        return Assignment.objects.filter(subjectRoom=self.subjectroom, due__lte=now).order_by('-due')

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


class TeacherAdminSharedFocusIdUtils(TeacherAdminSharedUtils):
    """
    ABSTRACT USAGE ONLY
    """

    def __init__(self, user, focusroom):
        super(TeacherAdminSharedFocusIdUtils, self).__init__(user)
        assert self.focus
        self.focusroom = focusroom

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(remedial__focusRoom=self.focusroom, due__gte=now).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        return Assignment.objects.filter(remedial__focusRoom=self.focusroom, due__lte=now).order_by('-due')

    def get_focusroom_reportcard_info(self):
        result = []
        students = self.focusroom.subjectRoom.students.all()
        now = django.utils.timezone.now()
        for student in students:
            average = Submission.objects.filter(student=student, assignment__remedial__focusRoom=self.focusroom,
                                                assignment__due__lte=now).aggregate(Avg("marks"))['marks__avg']
            result.append((student, average))
        return result

    def get_focusroom_average(self):
        return self.get_corrected_assignments().aggregate(Avg('average'))['average__avg']

## The following classes are for external use (because they contain user group checks)

class TeacherGroupUtils(object):
    """
    mixin to enable teacher user group checking
    """

    def __init__(self):
        self.UTILS_GROUP = HWCentralGroup.refs.TEACHER

class TeacherUtils(TeacherGroupUtils, TeacherAdminSharedUtils):
    def __init__(self, teacher):
        TeacherGroupUtils.__init__(self)
        TeacherAdminSharedUtils.__init__(self, teacher)

    def get_managed_classroom_ids(self):
        return self.user.classes_managed_set.values_list('pk', flat=True)

    def get_managed_subjectroom_ids(self):
        return self.user.subjects_managed_set.values_list('pk', flat=True)

    def get_managed_focusroom_ids(self):
        assert self.focus
        return FocusRoom.objects.filter(subjectRoom__teacher=self.user).values_list('pk', flat=True)

class TeacherSubjectIdUtils(TeacherGroupUtils, TeacherAdminSharedSubjectIdUtils):
    def __init__(self, teacher, subjectroom):
        TeacherGroupUtils.__init__(self)
        TeacherAdminSharedSubjectIdUtils.__init__(self, teacher, subjectroom)


class TeacherFocusIdUtils(TeacherGroupUtils, TeacherAdminSharedFocusIdUtils):
    def __init__(self, teacher, focusroom):
        TeacherGroupUtils.__init__(self)
        TeacherAdminSharedFocusIdUtils.__init__(self, teacher, focusroom)
