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

        self.listing = SidebarListingViewModel(user)

        # def get_listing_title(group):
        #     # NOTE: what follows is a pythonic switch statement
        #     # This is configuration, it should be moved to a config file which is loaded into memory at startup
        #     return {
        #         HWCentralGroup.ADMIN: 'Classrooms',
        #         HWCentralGroup.PARENT: 'Students',
        #         HWCentralGroup.STUDENT: 'Subjects',
        #         HWCentralGroup.TEACHER: 'Classrooms'
        #     }.get(group)


class SidebarListingViewModel():
    def __init__(self, user):
        self


class HomeViewModel(BaseViewModel):
    def __init__(self, sidebar, ):
        self.sidebar = sidebar

