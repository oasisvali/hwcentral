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


    def __init__(self, request):
        """
        Sets up the user and user_group for the View Driver, by examining the request
        """

        self.user = request.user
        self.user_group = self.user.userinfo.group.pk
        self.request = request

        # dervied class constructor must set the urlname member in its constructor - BEFORE calling handle
        self.urlname = None

        # this is generated in handle
        self.template = None


    def handle(self):
        """
        Calls the correct member view based on the group of the user who sent the request.
        Also sets the template path based on the user's group.
        """

        if self.urlname is None:
            raise NotImplementedError("Subclass of GroupDrivenView needs to set urlname.")

        if not hasattr(self, 'type'):
            self.type = None  # if type is not defined by the constructor of a deriving class

        if self.user_group == HWCentralGroup.STUDENT:
            self.template = self.urlname.get_group_driven_template('student', self.type)
            return self.student_view()
        elif self.user_group == HWCentralGroup.PARENT:
            self.template = self.urlname.get_group_driven_template('parent', self.type)
            return self.parent_view()
        elif self.user_group == HWCentralGroup.ADMIN:
            self.template = self.urlname.get_group_driven_template('admin', self.type)
            return self.admin_view()
        elif self.user_group == HWCentralGroup.TEACHER:
            self.template = self.urlname.get_group_driven_template('teacher', self.type)
            return self.teacher_view()
        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)