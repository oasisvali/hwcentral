from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render

from core.utils.toast import redirect_with_success_toast
from core.view_models.announcement import AnnouncementBody
from core.forms.announcement import AdminAnnouncementForm, ClassAnnouncementForm, ClassSubjectAnnouncementForm, \
    SubjectAnnouncementForm
from core.models import Announcement
from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import AdminSidebar, TeacherSidebar
from hwcentral.exceptions import InvalidStateError


class AnnouncementDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AnnouncementDriver, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT

    def student_endpoint(self):
        raise Http404  # TODO: error message?

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

        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user), AnnouncementBody(form))
                      .as_context() )

    def admin_endpoint(self):

        form = AdminAnnouncementForm()
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user), AnnouncementBody(form))
                      .as_context() )


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
                content_type = ContentType.objects.get(model="classroom")
                object_id = form.cleaned_data['classroom'].pk
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_type=content_type, object_id=object_id,
                                                               message=message, announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        elif (not classteacher) and subjectteacher :
            #For Subject Teacher type teacher user
            form = SubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="subjectroom")
                object_id = form.cleaned_data['subjectroom'].pk
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_type=content_type, object_id=object_id,
                                                               message=message, announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        elif classteacher and subjectteacher :
            #For a Class and Subject Teacher type teacher user
            form = ClassSubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                target = form.cleaned_data['target']
                if target.startswith(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):
                    object_id = long(target[len(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):])
                    content_type = ContentType.objects.get(model="subjectroom")
                elif target.startswith(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):
                    object_id = long(target[len(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):])
                    content_type = ContentType.objects.get(model="classroom")
                else:
                    raise InvalidStateError("Invalid announcement form target: %s" % target)
                message = form.cleaned_data['message']
                new_announcement = Announcement.objects.create(content_type=content_type, object_id=object_id,
                                                               message=message, announcer=self.user)
                return self.redirect_with_toast(new_announcement)
            else:
                return render(self.request, self.template,
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        else:
            raise Http404

    def admin_endpoint(self):

        form = AdminAnnouncementForm(self.request.POST)
        if form.is_valid():
            content_type = ContentType.objects.get(model="school")
            object_id = self.user.userinfo.school.pk
            message = form.cleaned_data['message']
            new_announcement = Announcement.objects.create(content_type=content_type, object_id=object_id,
                                                           message=message, announcer=self.user)
            return self.redirect_with_toast(new_announcement)
        else:
            return render(self.request, self.template,
                          AuthenticatedBase(AdminSidebar(self.user), AnnouncementBody(form))
                      .as_context() )
