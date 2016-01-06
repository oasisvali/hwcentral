from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from core.routing.urlnames import UrlNames

SUBMIT_SUCCESS_REDIRECT_URL = UrlNames.HOME.name


def redirect_with_success_toast(request, success_message):
    """
    A shortcut function for view drivers to perform both redirection and display a success message toast at the redirected page
    @param redirect_url_name: The url name to redirect to
    @param success_message: The success message to be displayed in the toast
    """

    messages.success(request, mark_safe(success_message))
    return redirect(SUBMIT_SUCCESS_REDIRECT_URL)


def render_with_success_toast(request, message, *args, **kwargs):
    messages.success(request, mark_safe(message))
    return render(request, *args, **kwargs)


def render_with_error_toast(request, message, *args, **kwargs):
    messages.error(request, mark_safe(message))
    return render(request, *args, **kwargs)
