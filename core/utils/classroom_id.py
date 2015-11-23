import django
from django.db.models import Avg

from core.models import SubjectRoom, Assignment, Submission
from core.utils.base import BaseUtils
from core.utils.teacher import UncorrectedAssignmentInfoMixin


class ClassroomIdUtils(UncorrectedAssignmentInfoMixin, BaseUtils):
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
        return Assignment.objects.filter(subjectRoom__pk__in=subjectroom_ids, due__lte=now).order_by('-due')[
               :ClassroomIdUtils.CORRECTED_ASSIGNMENTS_LIMIT]

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
