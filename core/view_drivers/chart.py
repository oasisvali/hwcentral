import django

from core.utils.json import HWCentralJsonResponse, Json404Response
from core.models import SubjectRoom, Submission
from core.utils.user_checks import is_student_classteacher_relationship, is_subjectroom_classteacher_relationship, \
    is_student_corrected_assignment_relationship, is_assignment_teacher_relationship, is_parent_child_relationship
from core.view_drivers.base import GroupDriven
from core.view_models.chart import StudentPerformance, PerformanceBreakdown, SubjectroomPerformanceBreakdown, \
    AssignmentPerformanceElement, AnonAssignmentPerformanceElement


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
        if self.student != self.user:
            return Json404Response()

        return self.student_chart_data()

    def parent_endpoint(self):
        #validation - the logged in parent should only see the chart of his/her child
        if not is_parent_child_relationship(self.user, self.student):
            return Json404Response()

        return self.student_chart_data()

    def admin_endpoint(self):
        #validation - the logged in admin should only see the student chart if student belongs to same school
        if self.user.userinfo.school != self.student.userinfo.school:
            return Json404Response()

        return self.student_chart_data()


class StudentChartGet(StudentChartGetBase):
    def student_chart_data(self):
        return HWCentralJsonResponse(StudentPerformance(self.student))

    def teacher_endpoint(self):
        # validation - the logged in classteacher should only see the student chart if student belongs to his/her class
        # subjectteacher does not see this chart

        # check if student belongs to the set of classes
        if not is_student_classteacher_relationship(self.student, self.user):
            return Json404Response()

        return self.student_chart_data()


class SingleSubjectStudentChartGet(StudentChartGetBase):
    def __init__(self, request, subjectroom, student):
        super(SingleSubjectStudentChartGet, self).__init__(request, student)
        self.subjectroom = subjectroom

    def student_chart_data(self):
        return HWCentralJsonResponse(PerformanceBreakdown(self.student, self.subjectroom))

    def teacher_endpoint(self):
        # validation - the logged in subjectteacher should only see the student chart if student belongs to his/her subjectroom
        # the logged in classteacher should only see the student chart if the student belongs to his/her class

        if is_student_classteacher_relationship(self.student, self.user):
            return self.student_chart_data()

        # check if teacher is managing the given subjectroom
        if self.subjectroom.teacher == self.user:
            return self.student_chart_data()

        return Json404Response()


class SubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, subjectroom):
        super(SubjectroomChartGet, self).__init__(request)
        self.subjectroom = subjectroom

    def single_subjectroom_data(self):
        return HWCentralJsonResponse(SubjectroomPerformanceBreakdown(self.subjectroom))

    def student_endpoint(self):
        return Json404Response()

    def parent_endpoint(self):
        return Json404Response()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the subjectroom chart if subjectroom belongs to same school
        if self.user.userinfo.school != self.subjectroom.classRoom.school:
            return Json404Response()

        return self.single_subjectroom_data()

    def teacher_endpoint(self):
        # validation - the logged in classteacher should only see the subjectroom chart if the subjectroom belongs to her classroom
        # the logged in subjectteacher should only see the subjectroom chart if he/she manages the subjectroom

        if is_subjectroom_classteacher_relationship(self.subjectroom, self.user):
            return self.single_subjectroom_data()

        # now check if user is a subjectteacher for this subjectroom
        if self.subjectroom.teacher == self.user:
            return self.single_subjectroom_data()

        return Json404Response()


# TODO: reduce duplication between the following 2 subjectroom charts
class SubjectTeacherSubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, subjectteacher):
        super(SubjectTeacherSubjectroomChartGet, self).__init__(request)
        self.subjectteacher = subjectteacher

    def all_subjectroom_data(self):
        chart_data = []
        for subjectroom in self.subjectteacher.subjects_managed_set.all():
            chart_data.append(SubjectroomPerformanceBreakdown(subjectroom))

        return HWCentralJsonResponse(chart_data)

    def student_endpoint(self):
        return Json404Response()

    def parent_endpoint(self):
        return Json404Response()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the subjectteacher's subjectrooms if the subjectteacher belongs to same school
        if self.user.userinfo.school != self.subjectteacher.userinfo.school:
            return Json404Response()

        return self.all_subjectroom_data()

    def teacher_endpoint(self):
        # validation - only the logged in subjectteacher should only see his/her own subjectrooms

        if self.user != self.subjectteacher:
            return Json404Response()

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

        return HWCentralJsonResponse(chart_data)

    def student_endpoint(self):
        return Json404Response()

    def parent_endpoint(self):
        return Json404Response()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the classteacher's classroom if the classteacher belongs to same school
        if self.user.userinfo.school != self.classteacher.userinfo.school:
            return Json404Response()

        return self.classroom_data()

    def teacher_endpoint(self):
        # validation - only the logged in classteacher should only see his/her own classroom

        if self.user != self.classteacher:
            return Json404Response()

        return self.classroom_data()


class AssignmentChartGet(GroupDrivenChart):
    def __init__(self, request, assignment):
        super(AssignmentChartGet, self).__init__(request)
        self.assignment = assignment

    def assignment_chart_data(self):
        chart_data = []
        for submission in Submission.objects.filter(assignment=self.assignment):
            chart_data.append(AssignmentPerformanceElement(submission))

        return HWCentralJsonResponse(chart_data)

    def anon_assignment_chart_data(self):
        chart_data = []
        for submission in Submission.objects.filter(assignment=self.assignment):
            chart_data.append(AnonAssignmentPerformanceElement(submission))

        return HWCentralJsonResponse(chart_data)

    def student_endpoint(self):
        if is_student_corrected_assignment_relationship(self.user, self.assignment):
            return self.anon_assignment_chart_data()
        return Json404Response()

    def parent_endpoint(self):
        # validation - the logged in parent should only see an anonymous assignment chart if the assignment has been
        # assigned to their child
        for child in self.user.home.children.all():
            if is_student_corrected_assignment_relationship(child, self.assignment):
                return self.anon_assignment_chart_data()

        return Json404Response()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the assignment chart if the assignment belongs to same school
        if self.user.userinfo.school != self.assignment.subjectRoom.classRoom.school:
            return Json404Response()

        return self.assignment_chart_data()

    def teacher_endpoint(self):
        # validation - teacher should only see assignment chart if she is classteacher/subjectteacher for the assignment's subjectroom

        if is_assignment_teacher_relationship(self.assignment, self.user):
            return self.assignment_chart_data()

        return Json404Response()


class StandardAssignmentChartGet(GroupDrivenChart):
    def __init__(self, request, assignment):
        super(StandardAssignmentChartGet, self).__init__(request)
        self.assignment = assignment

    # for full standard histogram, we always send anon data because it doesnt make sense to have tooltips for so many cells
    def anon_assignment_chart_data(self):
        chart_data = []
        for submission in Submission.objects.filter(
                assignment__assignmentQuestionsList=self.assignment.assignmentQuestionsList,
                assignment__subjectRoom__classRoom__school=self.assignment.subjectRoom.classRoom.school,
                assignment__subjectRoom__classRoom__standard=self.assignment.subjectRoom.classRoom.standard,
                assignment__due__lte=django.utils.timezone.now()):
            chart_data.append(AnonAssignmentPerformanceElement(submission))

        return HWCentralJsonResponse(chart_data)

    def student_endpoint(self):
        return Json404Response()

    def parent_endpoint(self):
        return Json404Response()

    def admin_endpoint(self):
        # validation - the logged in admin should only see the assignment chart if the assignment belongs to same school
        if self.user.userinfo.school != self.assignment.subjectRoom.classRoom.school:
            return Json404Response()

        return self.anon_assignment_chart_data()

    def teacher_endpoint(self):
        # validation - teacher should only see assignment chart if she is classteacher/subjectteacher for the assignment's subjectroom

        if is_assignment_teacher_relationship(self.assignment, self.user):
            return self.anon_assignment_chart_data()

        return Json404Response()
