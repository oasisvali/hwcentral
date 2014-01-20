from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core.modules.forms import UserInfoForm
from core.routing.url_names import UrlNames

# AUTH VIEWS

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
def home_get(request):
    return render(request, 'authenticated/home.html')