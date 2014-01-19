from core.viewmodels.base import BaseViewModel

# def get_UserInfo(user):
#     """
#     Helper method to obtain the UserInfo object associated with the provided User object
#     @return: The UserInfo object associated with the given user object
#     """
#
#     return UserInfo.objects.get()

class SidebarViewModel():
    def __init__(self, request):
        user = request.user
        self.user_group = user.userinfo.group.name
        self.user_fullname = user.first_name + ' ' + user.last_name

        self.user_group


class HomeViewModel(BaseViewModel):
    def __init__(self, sidebar, ):
        self.sidebar = sidebar

