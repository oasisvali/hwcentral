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


    # dervied class constructor must set the urlname member
    @property
    def urlname(self):
        raise NotImplementedError("Subclass of GroupDrivenView needs to set urlname.")


    def __init__(self, request, *args, **kwargs):

        self.user = request.user
        self.user_group = self.user.userinfo.group.pk
        self.request_args = args
        self.request_kwargs = kwargs

    def handle(self):
        """
        Calls the correct member view based on the group of the user who sent the request.
        Also sets the template path based on the user's group.
        """

        if self.user_group == HWCentralGroup.STUDENT:
            self.template = self.urlname.get_template(self, '/student')
            return self.student_view()
        elif self.user_group == HWCentralGroup.PARENT:
            self.template = self.urlname.get_template(self, '/parent')
            return self.parent_view()
        elif self.user_group == HWCentralGroup.ADMIN:
            self.template = self.urlname.get_template(self, '/admin')
            return self.admin_view()
        elif self.user_group == HWCentralGroup.TEACHER:
            self.template = self.urlname.get_template(self, '/teacher')
            return self.teacher_view()
        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)