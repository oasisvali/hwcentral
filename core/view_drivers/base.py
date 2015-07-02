from core.utils.constants import HWCentralGroup
from hwcentral.exceptions import InvalidHWCentralGroupException



class GroupDriven(object):
    """
    All view drivers that implement different logic based on group of request user will inherit from this
    """

    def student_endpoint(self):
        raise NotImplementedError("Subclass of GroupDriven needs to implement student_endpoint.")

    def parent_endpoint(self):
        raise NotImplementedError("Subclass of GroupDriven needs to implement parent_endpoint.")

    def admin_endpoint(self):
        raise NotImplementedError("Subclass of GroupDriven needs to implement admin_endpoint.")

    def teacher_endpoint(self):
        raise NotImplementedError("Subclass of GroupDriven needs to implement teacher_endpoint.")

    def __init__(self, request):
        """
        Sets up the user, user_group and request for the View Driver, by examining the request
        """

        self.user = request.user
        self.user_group = self.user.userinfo.group.pk
        self.request = request

    def handle(self):
        if self.user_group == HWCentralGroup.STUDENT:
            return self.student_endpoint()
        elif self.user_group == HWCentralGroup.PARENT:
            return self.parent_endpoint()
        elif self.user_group == HWCentralGroup.ADMIN:
            return self.admin_endpoint()
        elif self.user_group == HWCentralGroup.TEACHER:
            return self.teacher_endpoint()
        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)


class GroupDrivenView(GroupDriven):
    """
    Abstract class that provides common functionality required by all views which have different logic for different
    user group
    """

    def __init__(self, request):

        super(GroupDrivenView, self).__init__(request)

        # dervied class constructor must set the urlname member in its constructor - BEFORE calling handle
        self.urlname = None

        # this is generated in handle
        self.template = None

    def get_template(self,group):
        return self.urlname.get_group_driven_template(group,self.type)

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

            self.template = self.get_template('student')
            return self.student_endpoint()
        elif self.user_group == HWCentralGroup.PARENT:
            self.template = self.get_template('parent')
            return self.parent_endpoint()
        elif self.user_group == HWCentralGroup.ADMIN:
            self.template = self.get_template('admin')
            return self.admin_endpoint()
        elif self.user_group == HWCentralGroup.TEACHER:
            self.template = self.get_template('teacher')
            return self.teacher_endpoint()

        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)



class GroupDrivenViewCommonTemplate(GroupDrivenView):
    def get_template(self,group):
        # USELESS ARG GROUP!!!!! BECAUSE THIS DRIVER USES A COMMON TEMPLATE!!!!!!!
        return self.urlname.get_template()
