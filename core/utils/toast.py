from django.contrib import messages
from django.shortcuts import redirect

from core.routing.urlnames import UrlNames

SUBMIT_SUCCESS_REDIRECT_URL = UrlNames.HOME.name


def redirect_with_toast(request, success_message):
    """
    A shortcut function for view drivers to perform both redirection and display a success message toast at the redirected page
    @param redirect_url_name: The url name to redirect to
    @param success_message: The success message to be displayed in the toast
    """

    messages.add_message(request, messages.INFO, success_message)
    return redirect(SUBMIT_SUCCESS_REDIRECT_URL)
