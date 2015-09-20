from hwcentral.exceptions import InvalidHWCentralGroupError
from core.utils.references import HWCentralGroup


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

    def student_endpoint_setup(self):
        pass

    def parent_endpoint_setup(self):
        pass

    def admin_endpoint_setup(self):
        pass

    def teacher_endpoint_setup(self):
        pass

    def common_endpoint_setup(self):
        pass

    def __init__(self, request):
        """
        Sets up the user, user_group and request for the View Driver, by examining the request
        """

        self.user = request.user
        self.user_group = self.user.userinfo.group
        self.request = request

    def handle(self):

        self.common_endpoint_setup()

        if self.user_group == HWCentralGroup.refs.STUDENT:
            self.student_endpoint_setup()
            return self.student_endpoint()
        elif self.user_group == HWCentralGroup.refs.PARENT:
            self.parent_endpoint_setup()
            return self.parent_endpoint()
        elif self.user_group == HWCentralGroup.refs.ADMIN:
            self.admin_endpoint_setup()
            return self.admin_endpoint()
        elif self.user_group == HWCentralGroup.refs.TEACHER:
            self.teacher_endpoint_setup()
            return self.teacher_endpoint()
        else:
            raise InvalidHWCentralGroupError(self.user_group.name)

class GroupDrivenView(GroupDriven):
    """
    Abstract class that provides common functionality required by all views which have different logic for different
    user group
    """
    def __init__(self, request):

        super(GroupDrivenView, self).__init__(request)

        # dervied class constructor must set the urlname member in its constructor - BEFORE calling handle
        self.urlname = None

        # this is manipulated by child classes in setup functions
        self.template = None

    def handle(self):
        """
        Calls the correct member view based on the group of the user who sent the request.
        Also sets the template path based on the user's group.
        """

        if self.urlname is None:
            raise NotImplementedError("Subclass of GroupDrivenView needs to set urlname.")

        return super(GroupDrivenView, self).handle()


class GroupDrivenViewGroupDrivenTemplate(GroupDrivenView):
    """
    Abstract class that provides common functionality required by all views which have different logic and different
    templates for different user group
    """

    def common_endpoint_setup(self):
        self.template = self.urlname.get_template(self.user_group.name.lower())



class GroupDrivenViewCommonTemplate(GroupDrivenView):
    # Obviously, the urlname associated with a common template driver should also generate template without any args
    def common_endpoint_setup(self):
        self.template = self.urlname.get_template()


class GroupDrivenViewTypeDrivenTemplate(GroupDrivenView):
    def common_endpoint_setup(self):
        if self.type is None:
            raise NotImplementedError("Subclass of GroupDrivenViewTypeDrivenTemplate needs to set type.")

        self.template = self.urlname.get_template(self.type)
