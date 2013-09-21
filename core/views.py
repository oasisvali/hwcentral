from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from core.modules.constants import HttpMethod, UrlNames

# ROUTERS

# allow only get requests for the static router
from core.modules.forms import UserInfoForm


@require_safe
def static_router(request, template):
    assert template is not None
    return render(request, template)


def redirect_router(request, target_view_name):
    assert target_view_name is not None
    return redirect(target_view_name)


def dynamic_router(request, *args, **kwargs):
    get_view = kwargs.pop(HttpMethod.GET, None)
    post_view = kwargs.pop(HttpMethod.POST, None)
    put_view = kwargs.pop(HttpMethod.PUT, None)
    delete_view = kwargs.pop(HttpMethod.DELETE, None)

    if request.method == HttpMethod.GET and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == HttpMethod.POST and post_view is not None:
        return post_view(request, *args, **kwargs)
    elif request.method == HttpMethod.PUT and put_view is not None:
        return put_view(request, *args, **kwargs)
    elif request.method == HttpMethod.DELETE and delete_view is not None:
        return delete_view(request, *args, **kwargs)
    raise Http404

# AUTH CHECK WRAPPERS

def requires_auth_strict(view):
    """
    Use this wrapper method for views which MUST only be called while the user is authenticated (e.g. logout)
    @param view:
    @return:
    """

    def delegate_view(request, *args, **kwargs):
        assert request.user.is_authenticated()
        return view(request, *args, **kwargs)

    return delegate_view

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

@login_required
def home_get(request):
    return render(request, 'home.html')


    # USER PROFILE VIEWS (change pass. etc)

    #def register(request):
    #    return HttpResponse('Looking at Register')
    #
    #
    #def login(request):
    #    return HttpResponse('Looking at Login')
    #
    #
    #def classroom(request, id=None):
    #    return HttpResponse('Looking at Classroom')
    #
    #
    #def hw(request, id=None):
    #    return HttpResponse('Looking at Hw')
    #
    #
    #def submission(request, id=None):
    #    return HttpResponse('Looking at Submission')
    #
    #
    #def user(request, id=None):
    #    return HttpResponse('Looking at User')
    #
    #
    #def school(request, id=None):
    #    return HttpResponse('Looking at School. Id is: ' + str(id))
    #
    #
    #def board(request, id=None):
    #    return HttpResponse('Looking at Board')