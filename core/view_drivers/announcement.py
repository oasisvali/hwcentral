from django.http import Http404
from django.shortcuts import render

from core.forms.announcement import AdminAnnouncementForm, ClassAnnouncementForm, ClassSubjectAnnouncementForm, \
    SubjectAnnouncementForm
from core.models import Announcement, ClassRoom, SubjectRoom
from core.routing.urlnames import UrlNames
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.announcement import AnnouncementBody
from core.view_models.base import AuthenticatedVM
from hwcentral.exceptions import InvalidStateError


class AnnouncementDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AnnouncementDriver, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT

    def student_endpoint(self):
        raise Http404

    def open_student_endpoint(self):
        raise Http404

    def parent_endpoint(self):
        raise Http404


class AnnouncementGet(AnnouncementDriver):

    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.exists():
            classteacher = True
        if self.user.subjects_managed_set.exists():
            subjectteacher= True

        if classteacher and (not subjectteacher) :
            form = ClassAnnouncementForm(self.user)
        elif classteacher and subjectteacher:
            form = ClassSubjectAnnouncementForm(self.user)
        elif (not classteacher) and subjectteacher:
            form = SubjectAnnouncementForm(self.user)
        else:  # (not classteacher) and (not subjectteacher)
            raise Http404

        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   AnnouncementBody(form))
                      .as_context())

    def admin_endpoint(self):

        form = AdminAnnouncementForm()
        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   AnnouncementBody(form))
                      .as_context())


class AnnouncementPost(AnnouncementDriver):
    def redirect_with_toast(self, new_announcement):
        return redirect_with_success_toast(self.request,
                                           'Announcement for %s was created successfully.' % new_announcement.get_target_label())

    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.exists():
            classteacher = True
        if self.user.subjects_managed_set.exists():
            subjectteacher= True

        if classteacher and (not subjectteacher):
            #For ClassTeacher type teacher user
            form = ClassAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                classroom = form.cleaned_data['classroom']
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_object=classroom, message=message,
                                                               announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedVM(self.user,
                                              AnnouncementBody(form)).as_context())

        elif (not classteacher) and subjectteacher :
            #For Subject Teacher type teacher user
            form = SubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                subjectroom = form.cleaned_data['subjectroom']
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_object=subjectroom, message=message,
                                                               announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedVM(self.user,
                                              AnnouncementBody(form)).as_context())

        elif classteacher and subjectteacher :
            #For a Class and Subject Teacher type teacher user
            form = ClassSubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                target = form.cleaned_data['target']
                if target.startswith(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):
                    content_object = SubjectRoom.objects.get(
                        pk=long(target[len(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):]))
                elif target.startswith(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):
                    content_object = ClassRoom.objects.get(
                        pk=long(target[len(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):]))
                else:
                    raise InvalidStateError("Invalid announcement form target: %s" % target)
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_object=content_object,
                                                               message=message, announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedVM(self.user,
                                              AnnouncementBody(form)).as_context())

        else:
            raise Http404

    def admin_endpoint(self):

        form = AdminAnnouncementForm(self.request.POST)
        if form.is_valid():
            content_object = self.user.userinfo.school
            message = form.cleaned_data['message']
            new_announcement = Announcement.objects.create(content_object=content_object,
                                                           message=message, announcer=self.user)
            return self.redirect_with_toast(new_announcement)
        else:
            return render(self.request, self.template,
                          AuthenticatedVM(self.user, AnnouncementBody(form))
                          .as_context())
