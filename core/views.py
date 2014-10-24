import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Assignment, SubjectRoom
from core.utils.forms import UserInfoForm
from core.routing.urlnames import UrlNames
from core.view_drivers.assignments import AssignmentsGet
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar
from core.view_drivers.home import HomeGet
from core.view_drivers.settings import SettingsGet
from core.view_drivers.subject_id import SubjectIdGet

# TODO: condition checking for these views i.e., is the user allowed to see this page?
def register_get(request):
    user_form = UserCreationForm()
    user_info_form = UserInfoForm()
    return render(request, UrlNames.REGISTER.get_template(), {
        'user_form': user_form,
        'user_info_form': user_info_form
    })


def register_post(request):
    user_form = UserCreationForm(request.POST)
    user_info_form = UserInfoForm(request.POST)
    if user_form.is_valid() and user_info_form.is_valid():
        # save new user and bind the new user info to it
        new_user = user_form.save()
        new_user_info = user_info_form.save(commit=False)
        new_user_info.user = new_user
        new_user_info.save()

        # log user in
        login(request, new_user)
        return redirect(UrlNames.HOME.name)

    return render(request, UrlNames.REGISTER.get_template(), {
        'user_form': user_form,
        'user_info_form': user_info_form
    })


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
def test_get(request):
    return render(request, UrlNames.TEST.get_template(), AuthenticatedBase(StudentSidebar(request.user)).as_context())


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
def assignments_get(request):
    return AssignmentsGet(request).handle()


@login_required
def assignment_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # check if assignment is active or graded
    if assignment.due > datetime.now():
        return AssignmentIdActiveGet(request, assignment).handle()
    else:
        return AssignmentIdGradedGet(request, assignment).handle()


@login_required
def assignment_post(request, assignment_id):
    if assignment_id is None:
        raise Http404

    raise NotImplementedError()

# @login_required
# def school_get(request):
# raise NotImplementedError()
# @login_required
# def student_get(request):
# raise NotImplementedError()
# @login_required
# def classroom_get(request):
# raise NotImplementedError()
