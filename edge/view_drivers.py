from django.shortcuts import render

from core.utils.json import Json404Response, HWCentralJsonResponse
from core.utils.user_checks import is_student_classteacher_relationship, is_student_subjectteacher_relationship
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate, GroupDriven
from core.view_models.base import AuthenticatedVM
from edge.urlnames import EdgeUrlNames
from edge.view_models import StudentIndexBody, ParentIndexBody, TeacherIndexBody, AdminIndexBody, \
    StudentPositiveNegative, SubjectRoomPositiveNegative


class IndexGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request):
        super(IndexGet, self).__init__(request)
        self.urlname = EdgeUrlNames.INDEX

    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedVM(self.user, StudentIndexBody()).as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedVM(self.user, ParentIndexBody(self.user)).as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedVM(self.user, TeacherIndexBody(self.user)).as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedVM(self.user, AdminIndexBody(self.user)).as_context())


class SubjectIdGet(GroupDriven):
    def __init__(self, request, subjectroom):
        super(SubjectIdGet, self).__init__(request)
        self.subjectroom = subjectroom

    def student_endpoint(self):
        return Json404Response()

    def parent_endpoint(self):
        return Json404Response()

    def teacher_endpoint(self):
        if self.user == self.subjectroom.teacher or self.user == self.subjectroom.classRoom.classTeacher:
            return HWCentralJsonResponse(SubjectRoomPositiveNegative(self.subjectroom))
        return Json404Response()

    def admin_endpoint(self):
        if self.user.userinfo.school == self.subjectroom.classRoom.school:
            return HWCentralJsonResponse(SubjectRoomPositiveNegative(self.subjectroom))
        return Json404Response()


class StudentIdGet(GroupDriven):
    def __init__(self, request, student):
        super(StudentIdGet, self).__init__(request)
        self.student = student

    def student_endpoint(self):
        if self.user != self.student:
            return Json404Response()
        return HWCentralJsonResponse(StudentPositiveNegative(self.student))

    def parent_endpoint(self):
        if not self.user.home.children.filter(pk=self.student.pk).exists():
            return Json404Response()
        return HWCentralJsonResponse(StudentPositiveNegative(self.student))

    def teacher_endpoint(self):
        if is_student_classteacher_relationship(self.student, self.user) or is_student_subjectteacher_relationship(
                self.student, self.user):
            return HWCentralJsonResponse(StudentPositiveNegative(self.student))
        return Json404Response()

    def admin_endpoint(self):
        if self.user.userinfo.school == self.student.userinfo.school:
            return HWCentralJsonResponse(StudentPositiveNegative(self.student))
        return Json404Response()
