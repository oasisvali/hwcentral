from django.http import Http404
from django.shortcuts import render

from core.forms.open_classroom import OpenClassRoomForm
from core.forms.practice import OpenAssignmentForm
from core.routing.urlnames import UrlNames
from core.utils.references import HWCentralGroup, HWCentralOpen
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate
from core.view_models.base import AuthenticatedVM
from core.view_models.home import StudentHomeBody, TeacherHomeBody, ParentHomeBody, AdminHomeBody, OpenStudentHomeBody


class HomeGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request):
        super(HomeGet, self).__init__(request)
        self.urlname = UrlNames.HOME


    def student_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, StudentHomeBody(self.user))
                      .as_context())

    def open_student_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, OpenStudentHomeBody(self.user, OpenAssignmentForm(self.user)))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, TeacherHomeBody(self.user))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, ParentHomeBody(self.user))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, AdminHomeBody(self.user))
                      .as_context())


def change_open_student_classroom(open_student, classroom):
    assert open_student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT
    assert classroom.school == HWCentralOpen.refs.SCHOOL

    if open_student in classroom.students.all():
        return

    current_classroom = open_student.classes_enrolled_set.get()
    current_classroom.students.remove(open_student)
    for subjectroom in current_classroom.subjectroom_set.all():
        subjectroom.students.remove(open_student)

    classroom.students.add(open_student)
    for subjectroom in classroom.subjectroom_set.all():
        subjectroom.students.add(open_student)


class HomePost(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request):
        super(HomePost, self).__init__(request)
        self.urlname = UrlNames.HOME

    def student_endpoint(self):
        raise Http404

    def open_student_endpoint(self):
        form = OpenClassRoomForm(self.request.POST)
        if form.is_valid():
            new_classroom = form.cleaned_data['grade']
            # make changes to open student
            change_open_student_classroom(self.user, new_classroom)
            # reload
            return redirect_with_success_toast(self.request,
                                               "Your Grade level has been changed to %s. You can resume your saved state for your previous grade by changing back the Grade setting." % new_classroom.standard.number)

        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404
