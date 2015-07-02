from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from core.view_models.announcement import AnnouncementBody
from core.forms.announcement import AdminAnnouncementForm, ClassAnnouncementForm, ClassSubjectAnnouncementForm, \
    SubjectAnnouncementForm
from core.models import Announcement
from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import AdminSidebar, TeacherSidebar


class AnnouncementGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AnnouncementGet, self).__init__(request)
        self.user = request.user
        self.urlname = UrlNames.ANNOUNCEMENT
        self.request =request
        self.user_group = request.user.userinfo.group.pk
    def student_endpoint(self):
        return HttpResponseForbidden()
    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.count() >0 :
            classteacher = True
        if self.user.subjects_managed_set.count() >0:
            subjectteacher= True

        if classteacher and not subjectteacher :
            form = ClassAnnouncementForm(self.user)
        if classteacher and subjectteacher :
            form = ClassSubjectAnnouncementForm(self.user)
        if not classteacher and subjectteacher:
            form = SubjectAnnouncementForm(self.user)
        if not classteacher and not subjectteacher:
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
    def __init__(self, request):
        super(AnnouncementPost, self).__init__(request)
        self.user = request.user
        self.urlname = UrlNames.ANNOUNCEMENT
        self.request =request
        self.user_group = request.user.userinfo.group.pk

    def student_endpoint(self):
        return HttpResponseForbidden()

    def teacher_endpoint(self):
        classteacher=False
        subjectteacher = False
        if self.user.classes_managed_set.count()>0:
            classteacher = True
        if self.user.subjects_managed_set.count()>0:
            subjectteacher= True

        if classteacher and not subjectteacher:
            #For ClassTeacher type teacher user
            form = ClassAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="classroom")
                object_id = form.cleaned_data ['classroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        elif not classteacher and subjectteacher :
            #For Subject Teacher type teacher user
            form = SubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="subjectroom")
                object_id = form.cleaned_data ['subjectroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        elif classteacher and subjectteacher :
            #For a Class and Subject Teacher type teacher user
            form = ClassSubjectAnnouncementForm(self.user,self.request.POST)
            if form.is_valid():
                content_type = form.cleaned_data ['targets']
                if content_type[0] == "s":
                    object_id = content_type[1:len(content_type)]
                    content_type = ContentType.objects.get(model="subjectroom")
                    return redirect(UrlNames.HOME.name)
                elif content_type[0] == "c":
                    object_id = content_type[1:len(content_type)]
                    content_type = ContentType.objects.get(model="classroom")

                    message = form.cleaned_data ['message']
                    Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                    return redirect(UrlNames.HOME.name)
        else:
            return HttpResponseForbidden()
    def student_endpoint(self):
        return HttpResponseForbidden()
    def admin_endpoint(self):
        form = AdminAnnouncementForm(self.request.POST)
        if form.is_valid():
            return redirect(UrlNames.HOME.name)