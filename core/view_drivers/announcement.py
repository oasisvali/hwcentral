from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.http import Http404
from django.shortcuts import render, redirect

from core.view_models.announcement import AnnouncementBody

from core.forms.announcement import AdminAnnouncementForm, ClassAnnouncementForm, ClassSubjectAnnouncementForm, \
    SubjectAnnouncementForm
from core.models import Announcement
from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import AdminSidebar, TeacherSidebar
from hwcentral.exceptions import InvalidStateException


class AnnouncementGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AnnouncementGet, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT
    def student_endpoint(self):
        return HttpResponseForbidden()
    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.count() >0 :
            classteacher = True
        if self.user.subjects_managed_set.count() >0:
            subjectteacher= True

        if classteacher and (not subjectteacher) :
            form = ClassAnnouncementForm(self.user)
        if classteacher and subjectteacher :
            form = ClassSubjectAnnouncementForm(self.user)
        if (not classteacher) and subjectteacher:
            form = SubjectAnnouncementForm(self.user)
        if (not classteacher) and not subjectteacher:
            return HttpResponseForbidden()

        return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form))
                      .as_context() )
    def parent_endpoint(self):
        return HttpResponseForbidden()
    def admin_endpoint(self):

        form = AdminAnnouncementForm()
        return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),AuthenticatedBase(AdminSidebar(self.user),AnnouncementBody(form))
                      .as_context() )

class AnnouncementPost(GroupDrivenViewCommonTemplate):

    REDIRECT_TARGET = UrlNames.HOME.name
    def __init__(self, request):
        super(AnnouncementPost, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT

    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.count()>0:
            classteacher = True
        if self.user.subjects_managed_set.count()>0:

            subjectteacher= True

        if classteacher and (not subjectteacher):
            #For ClassTeacher type teacher user
            form = ClassAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="classroom")
                object_id = form.cleaned_data['classroom'].id
                message = form.cleaned_data['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(AnnouncementPost.REDIRECT_TARGET)
            else:
                return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        elif (not classteacher) and subjectteacher :
            #For Subject Teacher type teacher user
            form = SubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="subjectroom")
                object_id = form.cleaned_data['subjectroom'].id
                message = form.cleaned_data['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(AnnouncementPost.REDIRECT_TARGET)
            else:
                return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        elif classteacher and subjectteacher :
            #For a Class and Subject Teacher type teacher user
            form = ClassSubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                target = form.cleaned_data['target']
                if target.startswith(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):
                    object_id = target[len(ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX):]
                    content_type = ContentType.objects.get(model="subjectroom")
                elif target.startswith(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):
                    object_id = target[len(ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX):]
                    content_type = ContentType.objects.get(model="classroom")
                else:
                    raise InvalidStateException("Invalid announcement form target: %s" % target)
                message = form.cleaned_data['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(AnnouncementPost.REDIRECT_TARGET)
            else:
                return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),
                              AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form)).as_context() )

        else:
            return HttpResponseForbidden()

    def student_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):

        form = AdminAnnouncementForm(self.request.POST)
        content_type = ContentType.objects.get(model="school")
        object_id = self.user.userinfo.school.id
        message = form.cleaned_data ['message']
        Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
        if form.is_valid():
            return redirect(AnnouncementPost.REDIRECT_TARGET)
        else:
            return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),AuthenticatedBase(AdminSidebar(self.user),AnnouncementBody(form))
                      .as_context() )
