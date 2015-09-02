from django.http import HttpResponseNotFound
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.utils.user_checks import is_parent_child_relationship, is_subjectroom_student_relationship, \
    is_subjectroom_classteacher_relationship
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar
from core.view_models.subject_id import StudentSubjectIdBody, TeacherSubjectIdBody, AdminSubjectIdBody, \
    ParentSubjectIdBody
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate, GroupDrivenView


class SubjectIdGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request, subjectroom):
        super(SubjectIdGet, self).__init__(request)
        self.urlname = UrlNames.SUBJECT_ID
        self.subjectroom = subjectroom


    def student_endpoint(self):
        if not is_subjectroom_student_relationship(self.subjectroom, self.user):
            return HttpResponseNotFound()

        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentSubjectIdBody(self.user,
                                                                                                        self.subjectroom))
                      .as_context())

    def teacher_endpoint(self):
        if self.subjectroom.teacher != self.user and (
        not is_subjectroom_classteacher_relationship(self.subjectroom, self.user)):
            return HttpResponseNotFound()

        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherSubjectIdBody(self.user,
                                                                                                        self.subjectroom))
                      .as_context())

    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        if self.user.userinfo.school != self.subjectroom.classRoom.school:
            return HttpResponseNotFound()

        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminSubjectIdBody(self.user,
                                                                                                      self.subjectroom))
                      .as_context())


class ParentSubjectIdGet(GroupDrivenView):
    def __init__(self, request, subjectroom, child):
        super(ParentSubjectIdGet, self).__init__(request)
        self.urlname = UrlNames.SUBJECT_ID
        self.subjectroom = subjectroom
        self.child = child

    def parent_endpoint_setup(self):
        self.template = self.urlname.get_template('student')  # parent sees child's subject_id page

    def parent_endpoint(self):
        # validation: parent should only see this page if the have a home rel with the child
        if not is_parent_child_relationship(self.user, self.child):
            return HttpResponseNotFound()
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                     ParentSubjectIdBody(self.child,
                                                                                          self.subjectroom))
                      .as_context())

    def student_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        return HttpResponseNotFound()

    def teacher_endpoint(self):
        return HttpResponseNotFound()