from django.contrib import messages
from django.shortcuts import redirect, render

from core.routing.urlnames import UrlNames

SUBMIT_SUCCESS_REDIRECT_URL = UrlNames.HOME.name


def redirect_with_success_toast(request, success_message):
    """
    A shortcut function for view drivers to perform both redirection and display a success message toast at the redirected page
    @param redirect_url_name: The url name to redirect to
    @param success_message: The success message to be displayed in the toast
    """

    messages.success(request, success_message)
    return redirect(SUBMIT_SUCCESS_REDIRECT_URL)


def render_with_success_toast(request, message, *args, **kwargs):
    messages.success(request, message)
    return render(request, *args, **kwargs)


def render_with_error_toast(request, message, *args, **kwargs):
    messages.error(request, message)
    return render(request, *args, **kwargs)

def render_with_toast(request, level, message, *args, **kwargs):
    messages.add_message(request, level, message)
    return render(request, *args, **kwargs)
