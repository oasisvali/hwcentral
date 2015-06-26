import django
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms.announcement import PostModelForm
from core.models import Assignment, SubjectRoom, Announcement
from core.forms.user import UserInfoForm
from core.routing.urlnames import UrlNames
from core.view_drivers.assignment_id import AssignmentIdActiveGet, AssignmentIdGradedGet
from core.view_drivers.assignments import AssignmentsGet
from core.view_drivers.chart import StudentChartGet, SubjectroomChartGet
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
def post_form_upload(request):
    if request.method == 'GET':
        form = PostModelForm()
    else:
        # A POST request: Handle Form Upload
        form = PostModelForm(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            content_type = form.cleaned_data['content_type', 'Schoool']
            content_id = form.cleaned_data['content_id', '1000000']
            message = form.cleaned_data['message', '0os']
            post = Announcement.objects.create(content_type=content_type,
                                               content_id=content_id, message=message)
            return HttpResponseRedirect(reverse('Announcemen',
                                                kwargs={'post_id': post.id}))

    return render(request, 'authenticated/home/announcements.html', {
        'form': form,
    })


"""
def post_form_upload(request):
    iusername = request.user.userinfo.group_id
    #form = PostModelForm(iusername=iusername)
    if request.method == "GET":
        form = PostModelForm()
    elif request.method == "POST":

        form = PostModelForm(request.POST)
        k = form.is_valid()
        j = form.errors
        if form.is_valid():
            print "form is valid!! "
            announcement = Announcement()
            announcement.content_type = form.cleaned_data ['content_type']
            announcement.object_id =form.cleaned_data ['object_id']
            announcement.message = form.cleaned_data ['message']
            announcement.save()

    return render(request, 'authenticated/home/announcements.html', {
            'form': form, })
"""
@login_required
def subject_get(request, subject_id):
    subject = get_object_or_404(SubjectRoom, pk=subject_id)
    return SubjectIdGet(request, subject).handle()


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
        raise HttpResponseBadRequest()

    return AssignmentIdActiveGet(request, assignment).handle()


@login_required
def student_chart_get(request, student_id):
    return StudentChartGet(request, student_id).handle()


@login_required
def single_subject_student_chart_get(request, subjectroom_id, student_id):
    return SingleSubjectStudentChartGet(request, subjectroom_id, student_id).handle()


@login_required
def subjectroom_chart_get(request, subjectroom_id):
    return SubjectroomChartGet(request, subjectroom_id).handle()


@login_required
def subject_teacher_subjectroom_chart_get(request, subjectroom_id):
    return SubjectTeacherSubjectroomChartGet(request, subjectroom_id).handle()


@login_required
def class_teacher_subjectroom_chart_get(request, subjectroom_id):
    return ClassTeacherSubjectroomChartGet(request, subjectroom_id).handle()

# @login_required
# def school_get(request):
# raise NotImplementedError()
# @login_required
# def student_get(request):
# raise NotImplementedError()
# @login_required
# def classroom_get(request):
# raise NotImplementedError()
