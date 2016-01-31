import django
from django.db.models import Avg, Q

from core.models import SubjectRoom, Assignment, Submission
from core.utils.base import BaseUtils
from core.utils.labels import get_focusroom_label
from core.utils.teacher import UncorrectedAssignmentInfoMixin
from focus.models import FocusRoom


class ClassroomIdUtils(UncorrectedAssignmentInfoMixin, BaseUtils):
    def __init__(self, classroom):
        self.classroom = classroom

    def get_contained_room_labels(self):
        rooms = []
        for subjectroom in self.get_contained_subjectrooms():
            rooms.append(subjectroom.subject.name)
            rooms.append(get_focusroom_label(subjectroom.subject.name))

        return rooms

    def get_contained_subjectrooms(self):
        return SubjectRoom.objects.filter(classRoom=self.classroom).order_by('subject__name')

    def get_contained_focusrooms(self):
        return FocusRoom.objects.filter(subjectRoom__classRoom=self.classroom).order_by('subjectRoom__subject__name')

    def get_contained_subjectroom_ids(self):
        return self.get_contained_subjectrooms().values_list('pk', flat=True)

    def get_contained_focusroom_ids(self):
        return self.get_contained_focusrooms().values_list('pk', flat=True)

    def get_uncorrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_contained_subjectroom_ids()
        focusroom_ids = self.get_contained_focusroom_ids()

        return Assignment.objects.filter(
                (Q(subjectRoom__pk__in=subjectroom_ids) | Q(remedial__focusRoom__pk__in=focusroom_ids))
                & Q(due__gte=now)
        ).order_by('-due')

    def get_corrected_assignments(self):
        now = django.utils.timezone.now()
        subjectroom_ids = self.get_contained_subjectroom_ids()
        focusroom_ids = self.get_contained_focusroom_ids()

        return Assignment.objects.filter(
                (Q(subjectRoom__pk__in=subjectroom_ids) | Q(remedial__focusRoom__pk__in=focusroom_ids))
                & Q(due__lte=now)
        ).order_by('-due')

    def get_reportcard_row_info(self):
        results = []
        now = django.utils.timezone.now()
        for student in self.classroom.students.all():
            averages = []
            for subjectroom in self.get_contained_subjectrooms():
                averages.append(Submission.objects.filter(student=student, assignment__subjectRoom=subjectroom,
                                                          assignment__due__lte=now).aggregate(Avg('marks'))[
                                    'marks__avg'])
                averages.append(Submission.objects.filter(student=student,
                                                          assignment__remedial__focusRoom=subjectroom.focusroom,
                                                          assignment__due__lte=now).aggregate(Avg('marks'))[
                                    'marks__avg'])

            # dont really need the classroom check below but what the heck why not
            aggregate = Submission.objects.filter(
                    Q(student=student, assignment__due__lte=now) &
                    (Q(assignment__subjectRoom__classRoom=self.classroom) | Q(
                        assignment__remedial__focusRoom__subjectRoom_classRoom=self.classroom))
            ).aggregate(Avg('marks'))['marks__avg']
            results.append((student, averages, aggregate))

        return results

    def get_classroom_averages_by_subject(self):
        results = []
        now = django.utils.timezone.now()
        for subjectroom in self.get_contained_subjectrooms():
            results.append(Assignment.objects.filter(subjectRoom=subjectroom, due__lte=now).aggregate(Avg('average'))[
                               'average__avg'])
            results.append(Assignment.objects.filter(remedial__focusRoom=subjectroom.focusroom, due__lte=now).aggregate(
                Avg('average'))[
                               'average__avg'])

        return results

    def get_classroom_average(self):
        return self.get_corrected_assignments().aggregate(Avg('average'))['average__avg']
