from itertools import chain
import django
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, Http404
from django.contrib.contenttypes.models import ContentType
from core.models import Announcement, ClassRoom
from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Assignment, SubjectRoom, School
from core.forms.user import UserInfoForm
from core.routing.urlnames import UrlNames
from core.utils.constants import HWCentralGroup
from core.view_drivers.assignment_id import AssignmentIdActiveGet, AssignmentIdGradedGet
from core.view_drivers.assignments import AssignmentsGet

from core.view_drivers.chart import StudentChartGet, SubjectroomChartGet, SingleSubjectStudentChartGet, \
    SubjectTeacherSubjectroomChartGet, ClassTeacherSubjectroomChartGet, AssignmentChartGet
from core.view_drivers.classroom_id import ClassroomIdGet
from core.view_drivers.chart import StudentChartGet
from core.view_drivers.home import HomeGet
from core.view_drivers.settings import SettingsGet
from core.view_drivers.subject_id import SubjectIdGet



# TODO: condition checking for these views i.e., is the user allowed to see this page?

def render_register(request, user_creation_form, user_info_form):
    """
    A helper to reduce code duplication between different register HTTP methods (get/post)
    @param request:         The original request
    @param user_creation_form:       newly created / validated UserCreationForm instance
    @param user_info_form:  newly created / validated UserInfoForm instance
    @return: HTTPResponse returned by the render method
    """
    return render(request, UrlNames.REGISTER.get_template(), {
        'user_creation_form': user_creation_form,
        'user_info_form': user_info_form
    })


def register_get(request):
    return render_register(request, UserCreationForm(), UserInfoForm())


def register_post(request):
    user_creation_form = UserCreationForm(request.POST)
    user_info_form = UserInfoForm(request.POST)
    if user_creation_form.is_valid() and user_info_form.is_valid():
        # save new user and bind the new user info to it
        new_user = user_creation_form.save()
        new_user_info = user_info_form.save(commit=False)
        new_user_info.user = new_user
        new_user_info.save()

        # log user in
        login(request, new_user)
        return redirect(UrlNames.HOME.name)

    # else if both forms are not valid
    return render_register(request, user_creation_form, user_info_form)


# BUSINESS VIEWS

def index_get(request):
    """
    View that handles requests to the base url. If user is logged in, redirect to home,
    otherwise redirect to index
    @param request:
    @return:
    """

    if request.user.is_authenticated():
        return redirect(UrlNames.HOME.name)
        # just display the index template
    return render(request, UrlNames.INDEX.get_template())


@login_required
def home_get(request):
    return HomeGet(request).handle()


@login_required
def settings_get(request):
    return SettingsGet(request).handle()

@login_required
def subject_get(request, subject_id):
    subject = get_object_or_404(SubjectRoom, pk=subject_id)
    return SubjectIdGet(request, subject).handle()


@login_required
def classroom_get(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    return ClassroomIdGet(request, classroom).handle()


@login_required
def assignments_get(request):
    return AssignmentsGet(request).handle()


@login_required
def assignment_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # check if assignment is active or graded
    if assignment.due > django.utils.timezone.now():
        return AssignmentIdActiveGet(request, assignment).handle()
    else:
        return AssignmentIdGradedGet(request, assignment).handle()


@login_required
def assignment_post(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # only allow submissions for active assignments
    if assignment.due <= django.utils.timezone.now():
        return HttpResponseBadRequest()

    return AssignmentIdActiveGet(request, assignment).handle()


def check_student(student):
    """
    Checks if object passed in is a student user, otherwise raises 404
    """
    if student.userinfo.group != HWCentralGroup.STUDENT:
        raise Http404


def check_subjectteacher(subjectteacher):
    """
    Checks if object passed in is a subjectteacher user, otherwise raises 404
    """
    if subjectteacher.userinfo.group != HWCentralGroup.TEACHER or subjectteacher.subjects_managed_set.count() == 0:
        raise Http404


# def check_classteacher(classteacher):
# """
#     Checks if object passed in is a classteacher user, otherwise raises 404
#     """
#     if classteacher.userinfo.group != HWCentralGroup.TEACHER or classteacher.classes_managed_set.count() == 0:
#         raise Http404


@login_required
def student_chart_get(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    check_student(student)
    return StudentChartGet(request, student).handle()



@login_required
def single_subject_student_chart_get(request, subjectroom_id, student_id):
    student = get_object_or_404(User, pk=student_id)
    check_student(student)
    subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)

    # check if provided student belongs to the provided subjectroom
    try:
        subjectroom.students.get(pk=student.pk)
    except User.DoesNotExist:
        raise Http404

    return SingleSubjectStudentChartGet(request, subjectroom, student).handle()
class AdminAnnouncementForm(forms.Form):
        message = forms.CharField()

@login_required
def subjectroom_chart_get(request, subjectroom_id):
    subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    return SubjectroomChartGet(request, subjectroom).handle()


@login_required
def subject_teacher_subjectroom_chart_get(request, subjectteacher_id):
    subjectteacher = get_object_or_404(User, pk=subjectteacher_id)
    check_subjectteacher(subjectteacher)
    return SubjectTeacherSubjectroomChartGet(request, subjectteacher).handle()


@login_required
def class_teacher_subjectroom_chart_get(request, classteacher_id, classroom_id):
    classteacher = get_object_or_404(User, pk=classteacher_id)
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    if classteacher.userinfo.group != HWCentralGroup.TEACHER or classroom.classTeacher != classteacher:
        raise Http404
    return ClassTeacherSubjectroomChartGet(request, classteacher, classroom).handle()


@login_required
def assignment_chart_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # only allow for graded assignments
    if assignment.due < django.utils.timezone.now():
        raise Http404
    return AssignmentChartGet(request, assignment).handle()
class ClassAnnouncementForm(forms.Form):
        def __init__(self,classTeacher):
            super(ClassAnnouncementForm,self).__init__()
            self.fields['classroom'] =forms.ModelChoiceField(queryset=ClassRoom.objects.filter(classTeacher=classTeacher))

        message = forms.CharField()

class SubjectAnnouncementForm(forms.Form):
        def __init__(self,classTeacher):
            super(SubjectAnnouncementForm,self).__init__()
            self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=classTeacher))

        message = forms.CharField()

class ClassSubjectAnnouncementForm(forms.Form):
        def __init__(self,classTeacher,*args,**kwargs):
            classTeacher = kwargs.get('classTeacher',0)
            super(ClassSubjectAnnouncementForm,self).__init__(*args,**kwargs)
            j =[]
            for subject in SubjectRoom.objects.filter(teacher=classTeacher):
                k = str(subject.subject_id),str(subject)
                j.append(k)
            for classes in ClassRoom.objects.filter(classTeacher=classTeacher):
                k = str(classes.classTeacher_id),str(classes)
                j.append(k)
            self.fields['targets'] =forms.ChoiceField(choices=j)

        message = forms.CharField()




@login_required
def announcement_get(request):

    if request.POST:
        userpk= request.user.userinfo.group_id
        userschool = request.user.userinfo.school.name
        classteacher=0
        subjectteacher = 0
        if request.user.classes_managed_set.count()>0:
            classteacher = 1
        if request.user.subjects_managed_set.count()>0:
            subjectteacher= 1

        if userpk == 4:
            form = AdminAnnouncementForm(request.POST)

            if form.is_valid():
                content_type = ContentType.objects.get(model="school")
                object_id = School.objects.get(name = userschool).id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)

                return redirect(UrlNames.HOME.name)

        if userpk == 2 and classteacher == 1 and subjectteacher == 0:
            form = ClassAnnouncementForm(request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="classroom")
                object_id = form.cleaned_data ['classroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        if userpk == 2 and classteacher == 0 and subjectteacher == 1:
            form = SubjectAnnouncementForm(request.POST)
            if form.is_valid():
                content_type = ContentType.objects.get(model="subjectroom")
                object_id = form.cleaned_data ['subjectroom'].id
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)

        if userpk == 2 and classteacher == 1 and subjectteacher == 1:
            form = ClassSubjectAnnouncementForm(request.POST )
            if form.is_valid():
                content_type = form.cleaned_data ['target']
                object_id = form.cleaned_data ['Room']
                message = form.cleaned_data ['message']
                Announcement.objects.create(content_type=content_type,object_id=object_id,message=message)
                return redirect(UrlNames.HOME.name)
    else:

        userpk= request.user.userinfo.group_id
        classteacher=0 #flags for class and subject teacher
        subjectteacher = 0
        teacherpk = int(request.user.id)

        if request.user.classes_managed_set.count() >0 :
            classteacher = 1
        if request.user.subjects_managed_set.count() >0:
            subjectteacher= 1

        if userpk == 4:
            form = AdminAnnouncementForm()
        if userpk == 2:
            if classteacher == 1:
                if subjectteacher == 0:

                    form = ClassAnnouncementForm(request.user)
                if subjectteacher == 1:
                    form = ClassSubjectAnnouncementForm(classTeacher=request.user)


            if classteacher == 0:
                if subjectteacher == 1:
                    form = SubjectAnnouncementForm(request.user)

    return render(request, UrlNames.ANNOUNCEMENT.get_template(), {'form': form})

# @login_required
# def school_get(request):
# raise NotImplementedError()
# @login_required
# def student_get(request):
# raise NotImplementedError()
# @login_required
# def classroom_get(request):
# raise NotImplementedError()
