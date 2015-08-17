# TODO: Later this wrapper should not cause an error to be thrown, it should only redirect to index.
# Keep the assert for now only to avoid unexpected state during active development
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


def requires_noauth_strict(view):
    """
    Use this wrapper method for views which MUST only be called while the user is not authenticated (e.g. forgot_password)
    """

    def delegate_view(request, *args, **kwargs):
        assert not request.user.is_authenticated()
        return view(request, *args, **kwargs)

    return delegate_view
