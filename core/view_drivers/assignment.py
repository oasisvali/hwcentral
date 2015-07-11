from django.http import HttpResponseForbidden

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate


class AssignmentDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AssignmentDriver, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT

    def student_endpoint(self):
        return HttpResponseForbidden()

    def parent_endpoint(self):
        return HttpResponseForbidden()

    def admin_endpoint(self):
        return HttpResponseForbidden()


class AssignmentGet(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        pass


class AssignmentPost(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        pass