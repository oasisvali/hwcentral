from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from core.announcement import AnnouncementBody
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

    def student_view(self):
        raise Http404

    def teacher_view(self):
        classteacher=False
        subjectteacher = False
        if self.request.user.classes_managed_set.count() >0 :
            classteacher = True
        if self.request.user.subjects_managed_set.count() >0:
            subjectteacher= True

        if classteacher :
            if not subjectteacher :
                form = ClassAnnouncementForm(self.request.user)
            if subjectteacher :
                form = ClassSubjectAnnouncementForm(self.request.user)
        elif not classteacher:
            if subjectteacher:
                form = SubjectAnnouncementForm(self.request.user)
            else:
                raise Http404
        return render(self.request, UrlNames.ANNOUNCEMENT.get_template(),AuthenticatedBase(TeacherSidebar(self.user),AnnouncementBody(form))
                      .as_context() )
    def parent_view(self):
        raise Http404

    def admin_view(self):
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

    def student_view(self):
        raise Http404

    def teacher_view(self):
        userschool = self.request.user.userinfo.school
        classteacher=False
        subjectteacher = False
        if self.request.user.classes_managed_set.count()>0:
            classteacher = True
        if self.request.user.subjects_managed_set.count()>0:
            subjectteacher= True

        if classteacher and not subjectteacher:
            #For ClassTeacher type teacher user
            form = ClassAnnouncementForm(self.request.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="classroom")
                object_id = form.cleaned_data ['classroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        elif not classteacher and subjectteacher :
            #For Subject Teacher type teacher user
            form = SubjectAnnouncementForm(self.request.user,self.request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="subjectroom")
                object_id = form.cleaned_data ['subjectroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        elif classteacher and subjectteacher :
            #For a Class and Subject Teacher type teacher user
            form = ClassSubjectAnnouncementForm(self.request.user,self.request.POST)
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
            raise Http404
    def student_view(self):
        raise Http404
    def admin_view(self):
        form = AdminAnnouncementForm(self.request.POST)
        if form.is_valid():
            return redirect(UrlNames.HOME.name)