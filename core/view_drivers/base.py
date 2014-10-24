from core.utils.constants import HWCentralGroup
from hwcentral.exceptions import InvalidHWCentralGroupException


class GroupDrivenView(object):
    """
    Abstract class that provides common functionality required by all views which have different logic for different
    user group
    """

    def student_view(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to implement student_view.")

    def parent_view(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to implement parent_view.")

    def admin_view(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to implement admin_view.")

    def teacher_view(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to implement teacher_view.")


    # dervied class constructor must set the urlname member in its constructor - BEFORE calling handle
    @property
    def urlname(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to set urlname.")


    def __init__(self, request):
        """
        Sets up the user and user_group for the View Driver, by examining the request
        """

        self.user = request.user
        self.user_group = self.user.userinfo.group.pk


    def handle(self):
        """
        Calls the correct member view based on the group of the user who sent the request.
        Also sets the template path based on the user's group.
        """
        type = ''
        if hasattr(self, 'type'):
            type = self.type  # if type is defined by the constructor of a deriving class, it will be set in urlname

        if self.user_group == HWCentralGroup.STUDENT:
            self.urlname.set_group('student').set_type(type)
            return self.student_view()
        elif self.user_group == HWCentralGroup.PARENT:
            self.urlname.set_group('parent').set_type(type)
            return self.parent_view()
        elif self.user_group == HWCentralGroup.ADMIN:
            self.urlname.set_group('admin').set_type(type)
            return self.admin_view()
        elif self.user_group == HWCentralGroup.TEACHER:
            self.urlname.set_group('teacher').set_type(type)
            return self.teacher_view()
        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)