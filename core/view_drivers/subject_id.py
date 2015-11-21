from django.http import Http404
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.utils.user_checks import is_parent_child_relationship, is_subjectroom_student_relationship, \
    is_subjectroom_classteacher_relationship
from core.view_models.base import AuthenticatedVM
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
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user, StudentSidebar(self.user),
                                                                   StudentSubjectIdBody(self.user,
                                                                                          self.subjectroom))
                      .as_context())

    def teacher_endpoint(self):
        if self.subjectroom.teacher != self.user and (
        not is_subjectroom_classteacher_relationship(self.subjectroom, self.user)):
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user, TeacherSidebar(self.user),
                                                                   TeacherSubjectIdBody(self.user,
                                                                                          self.subjectroom))
                      .as_context())

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        if self.user.userinfo.school != self.subjectroom.classRoom.school:
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user, AdminSidebar(self.user),
                                                                   AdminSubjectIdBody(self.user,
                                                                                        self.subjectroom))
                      .as_context())


class ParentSubjectIdGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request, subjectroom, child):
        super(ParentSubjectIdGet, self).__init__(request)
        self.urlname = UrlNames.SUBJECT_ID
        self.subjectroom = subjectroom
        self.child = child

    def parent_endpoint(self):
        # validation: parent should only see this page if the have a home rel with the child
        if not is_parent_child_relationship(self.user, self.child):
            raise Http404
        return render(self.request, self.template, AuthenticatedVM(self.user, ParentSidebar(self.user),
                                                                   ParentSubjectIdBody(self.child,
                                                                                         self.subjectroom))
                      .as_context())

    def student_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404
