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
