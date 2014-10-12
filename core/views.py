from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.models import ClassRoom

from core.modules.constants import HWCentralGroup
from core.modules.forms import UserInfoForm
from core.modules.utils.student_utils import get_num_unfinished_assignments
from core.routing.urlnames import UrlNames
from core.view_models.home import Home as HomeViewModel, AdminAuthenticatedBody, ParentAuthenticatedBody, \
    StudentAuthenticatedBody, TeacherAuthenticatedBody
from core.view_models.sidebar import TeacherClassroomsSidebarListing, Ticker, StudentSidebarListing, Sidebar, \
    ParentSidebarListing, AdminSidebarListing, TeacherSubjectsSidebarListing
from hwcentral.exceptions import InvalidStateException


def register_get(request):
    user_form = UserCreationForm()
    user_info_form = UserInfoForm()
    return render(request, UrlNames.REGISTER.template, {
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

    return render(request, UrlNames.REGISTER.template, {
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
    return render(request, UrlNames.INDEX.template)


@login_required
def test_get(request):
    return render(request, UrlNames.TEST.template, HomeViewModel(request.user).as_context())


@login_required
def home_get(request):
    user = request.user
    user_group = user.userinfo.group.pk
    sidebar_listings = []

    if user_group == HWCentralGroup.STUDENT:
        ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENT.name, get_num_unfinished_assignments(user))
        if user.subjects_enrolled_set.count() > 0:
            sidebar_listings.append(StudentSidebarListing(user))
        return render(request, 'authenticated/home/student.html',
                      HomeViewModel(Sidebar(user, sidebar_listings, ticker),
                                    StudentAuthenticatedBody(user)).as_context())

    elif user_group == HWCentralGroup.PARENT:
        if user.home.students.count() > 0:
            sidebar_listings.append(ParentSidebarListing(user))
        return render(request, 'authenticated/home/parent.html',
                      HomeViewModel(Sidebar(user, sidebar_listings), ParentAuthenticatedBody(user)).as_context())

    elif user_group == HWCentralGroup.ADMIN:
        if ClassRoom.objects.filter(school=user.userinfo.school).count() > 0:
            sidebar_listings.append(AdminSidebarListing(user))
        return render(request, 'authenticated/home/admin.html',
                      HomeViewModel(Sidebar(user, sidebar_listings), AdminAuthenticatedBody(user)).as_context())

    elif user_group == HWCentralGroup.TEACHER:
        if user.classes_managed_set.count() > 0:
            sidebar_listings.append(TeacherClassroomsSidebarListing(user))
        if user.subjects_managed_set.count() > 0:
            sidebar_listings.append(TeacherSubjectsSidebarListing(user))
        return render(request, 'authenticated/home/teacher.html',
                      HomeViewModel(Sidebar(user, sidebar_listings), TeacherAuthenticatedBody(user)).as_context())
    else:
        raise InvalidStateException('Invalid HWCentralGroup: %s' % user.userinfo.group.name)


# TODO: condition checking for these views i.e., is the user allowed to see this page?
@login_required
def student_get(request):
    raise NotImplementedError()


@login_required
def classroom_get(request):
    raise NotImplementedError()


@login_required
def subject_get(request):
    raise NotImplementedError()


@login_required
def assignment_get(request, id=None):
    raise NotImplementedError()


@login_required
def school_get(request):
    raise NotImplementedError()


@login_required
def settings_get(request):
    raise NotImplementedError()