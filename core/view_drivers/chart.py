from django.http import JsonResponse, HttpResponseForbidden

from core.models import SubjectRoom, ClassRoom, Submission

from core.view_drivers.base import GroupDriven
from core.view_models.chart import StudentPerformance, PerformanceBreakdown, SubjectroomPerformanceBreakdown, \
    AssignmentPerformanceElement


class GroupDrivenChart(GroupDriven):
    """
    Abstract class that provides common functionality required by all charts data endpoints which have different logic
    for different user group
    """


class StudentChartGetBase(GroupDrivenChart):
    def student_chart_data(self):
        raise NotImplementedError("Subclass of StudentChartGetBase needs to implement student_chart_data.")

    def __init__(self, request, student):
        super(StudentChartGetBase, self).__init__(request)
        self.student = student

    def student_endpoint(self):
        # validation - only the logged in student should be able to see his/her own chart
        if self.student.pk != self.user.pk:
            return HttpResponseForbidden()

        return self.student_chart_data()()

    def parent_endpoint(self):
        #validation - the logged in parent should only see the chart of his/her child
        if not self.user.home.students.filter(pk=self.student.pk).exists():
            return HttpResponseForbidden()

        return self.student_chart_data()

    def admin_endpoint(self):
        #validation - the logged in admin should only see the student chart if student belongs to same school
        if self.user.userinfo.school != self.student.userinfo.school:
            return HttpResponseForbidden()

        return self.student_chart_data()


def is_student_classteacher_relationship(student, classteacher):
    try:
        classteacher.classes_managed_set.get(pk=student.classes_enrolled_set.get().pk)
    except ClassRoom.DoesNotExist:
        return False

    return True


def is_subjectroom_classteacher_relationship(subjectroom, classteacher):
    try:
        classteacher.classes_managed_set.get(pk=subjectroom.classRoom.pk)
    except ClassRoom.DoesNotExist:
        return False

    return True


class StudentChartGet(StudentChartGetBase):
    def student_chart_data(self):
        return JsonResponse(StudentPerformance(self.student))

    def teacher_endpoint(self):
        # validation - the logged in classteacher should only see the student chart if student belongs to his/her class
        # subjectteacher does not see this chart

        # check if student belongs to the set of classes
        if not is_student_classteacher_relationship(self.student, self.user):
            return HttpResponseForbidden()

        return self.student_chart_data()


class SingleSubjectStudentChartGet(StudentChartGetBase):
    def __init__(self, request, subjectroom, student):
        super(SingleSubjectStudentChartGet, self).__init__(request, student)
        self.subjectroom = subjectroom

    def student_chart_data(self):
        return JsonResponse(PerformanceBreakdown(self.student, self.subjectroom))

    def teacher_endpoint(self):
        # validation - the logged in subjectteacher should only see the student chart if student belongs to his/her subjectroom
        # the logged in classteacher should only see the student chart if the student belongs to his/her class

        if is_student_classteacher_relationship(self.student, self.user):
            return self.student_chart_data()

        # check if teacher is managing the given subjectroom
        if self.subjectroom.teacher == self.user:
            return self.student_chart_data()

        return HttpResponseForbidden()


class SubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, subjectroom):
        super(SubjectroomChartGet, self).__init__(request)
        self.subjectroom = subjectroom

    def single_subjectroom_data(self):
        return JsonResponse([SubjectroomPerformanceBreakdown(self.subjectroom)])

    def student_endpoint(self):
        return HttpResponseForbidden()

    def parent_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the subjectroom chart if subjectroom belongs to same school
        if self.user.userinfo.school != self.subjectroom.classRoom.school:
            return HttpResponseForbidden()

        return self.single_subjectroom_data()

    def teacher_endpoint(self):
        # validation - the logged in classteacher should only see the subjectroom chart if the subjectroom belongs to her classroom
        # the logged in subjectteacher should only see the subjectroom chart if he/she manages the subjectroom

        if is_subjectroom_classteacher_relationship(self.subjectroom, self.user):
            return self.single_subjectroom_data()

        # now check if user is a subjectteacher for this subjectroom
        if self.subjectroom.teacher.pk == self.user.pk:
            return self.single_subjectroom_data()

        return HttpResponseForbidden()


# TODO: reduce duplication between the following 2 subjectroom charts
class SubjectTeacherSubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, subjectteacher):
        super(SubjectTeacherSubjectroomChartGet, self).__init__(request)
        self.subjectteacher = subjectteacher

    def all_subjectroom_data(self):
        chart_data = []
        for subjectroom in self.subjectteacher.subject_managed_set.all():
            chart_data.append(SubjectroomPerformanceBreakdown(subjectroom))

        return JsonResponse(chart_data)

    def student_endpoint(self):
        return HttpResponseForbidden()

    def parent_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the subjectteacher's subjectrooms if the subjectteacher belongs to same school
        if self.user.userinfo.school != self.subjectteacher.userinfo.school:
            return HttpResponseForbidden()

        return self.all_subjectroom_data()

    def teacher_endpoint(self):
        # validation - only the logged in subjectteacher should only see his/her own subjectrooms

        if self.user != self.subjectteacher:
            return HttpResponseForbidden()

        return self.all_subjectroom_data()


class ClassTeacherSubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, classteacher, classroom):
        super(ClassTeacherSubjectroomChartGet, self).__init__(request)
        self.classteacher = classteacher
        self.classroom = classroom

    def classroom_data(self):
        chart_data = []
        for subjectroom in SubjectRoom.objects.filter(classRoom=self.classroom):
            chart_data.append(SubjectroomPerformanceBreakdown(subjectroom))

        return JsonResponse(chart_data)

    def student_endpoint(self):
        return HttpResponseForbidden()

    def parent_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the classteacher's classroom if the classteacher belongs to same school
        if self.user.userinfo.school != self.classteacher.userinfo.school:
            return HttpResponseForbidden()

        return self.classroom_data()

    def teacher_endpoint(self):
        # validation - only the logged in classteacher should only see his/her own classroom

        if self.user != self.classteacher:
            return HttpResponseForbidden()

        return self.classroom_data()


class AssignmentChartGet(GroupDrivenChart):
    def __init__(self, request, assignment):
        super(AssignmentChartGet, self).__init__(request)
        self.assignment = assignment

    def assignment_chart_data(self):
        chart_data = []
        for submission in Submission.objects.filter(assignment=self.assignment):
            chart_data.append(AssignmentPerformanceElement(submission))

        return JsonResponse(chart_data)

    def student_endpoint(self):
        return HttpResponseForbidden()

    def parent_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the assignment chart if the assignment belongs to same school
        if self.user.userinfo.school != self.assignment.subjectRoom.classRoom.school:
            return HttpResponseForbidden()

        return self.assignment_chart_data()

    def teacher_endpoint(self):
        # validation - teacher should only see assignment chart if she is classteacher/subjectteacher for the assignment's subjectteacher

        if is_subjectroom_classteacher_relationship(self.assignment.subjectRoom, self.user):
            return self.assignment_chart_data()

        # now check if user is a subjectteacher for this subjectroom
        if self.assignment.subjectRoom.teacher.pk == self.user.pk:
            return self.assignment_chart_data()

        return HttpResponseForbidden()


