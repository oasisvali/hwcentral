from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe

from core.utils.constants import HttpMethod


@require_safe  # allow only get/head requests for the static router
def static_router(request, template):
    assert template is not None
    return render(request, template)


@require_safe
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