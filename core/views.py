from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core.modules.forms import UserInfoForm
from core.modules.routing_util import UrlNames

# AUTH VIEWS (TODO: make these ajax)

def register_get(request):
    user_form = UserCreationForm()
    user_info_form = UserInfoForm()
    return render(request, 'register.html', {
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

    return render(request, 'register.html', {
        'user_form': user_form,
        'user_info_form': user_info_form
    })

# BUSINESS VIEWS

def site_anchor_get(request):
    """
    View that handles clicks on the site_anchor (site banner). If user is logged in, redirect to home,
    otherwise redirect to index
    @param request:
    @return:
    """

    target_view_name = UrlNames.INDEX.name
    if request.user.is_authenticated():
        target_view_name = UrlNames.HOME.name

    return redirect(target_view_name)


@login_required
def home_get(request):
    return render(request, 'home.html')