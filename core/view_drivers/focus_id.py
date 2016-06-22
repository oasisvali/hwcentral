from django.http import Http404
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.utils.user_checks import is_parent_child_relationship, is_subjectroom_student_relationship, \
    is_subjectroom_classteacher_relationship
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate
from core.view_models.base import AuthenticatedVM
from core.view_models.focus_id import StudentFocusIdBody, TeacherFocusIdBody, AdminFocusIdBody, ParentFocusIdBody


class FocusIdGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request, focusroom):
        super(FocusIdGet, self).__init__(request)
        self.urlname = UrlNames.FOCUS_ID
        self.focusroom = focusroom

    def student_endpoint(self):
        if not is_subjectroom_student_relationship(self.focusroom.subjectRoom, self.user):
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   StudentFocusIdBody(self.user,
                                                                                      self.focusroom))
                      .as_context())

    def teacher_endpoint(self):
        if self.focusroom.subjectRoom.teacher != self.user and (
                not is_subjectroom_classteacher_relationship(self.focusroom.subjectRoom, self.user)):
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   TeacherFocusIdBody(self.user,
                                                                                      self.focusroom))
                      .as_context())

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        if self.user.userinfo.school != self.focusroom.subjectRoom.classRoom.school:
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   AdminFocusIdBody(self.user,
                                                                                    self.focusroom))
                      .as_context())

    def open_student_endpoint(self):
        raise Http404

class ParentFocusIdGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request, focusroom, child):
        super(ParentFocusIdGet, self).__init__(request)
        self.urlname = UrlNames.FOCUS_ID
        self.focusroom = focusroom
        self.child = child

    def parent_endpoint(self):
        # validation: parent should only see this page if the have a home rel with the child
        if not is_parent_child_relationship(self.user, self.child):
            raise Http404
        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   ParentFocusIdBody(self.child,
                                                                                     self.focusroom))
                      .as_context())

    def student_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def open_student_endpoint(self):
        raise Http404
