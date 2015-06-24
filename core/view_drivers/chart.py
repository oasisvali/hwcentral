from django.contrib.auth.models import User
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from core.models import SubjectRoom
from core.utils.constants import HWCentralGroup
from core.view_models.chart import StudentPerformance, PerformanceBreakdown


# TODO: surely has some common stuff with groupdrivenview
from hwcentral.exceptions import InvalidHWCentralGroupException


class GroupDrivenChart(object):
    """
    Abstract class that provides common functionality required by all charts data endpoints which have different logic
    for different user group
    """

    def student_view(self):
        raise NotImplementedError("Subclass of GroupDrivenChart needs to implement student_view.")

    def parent_view(self):
        raise NotImplementedError("Subclass of GroupDrivenChart needs to implement parent_view.")

    def admin_view(self):
        raise NotImplementedError("Subclass of GroupDrivenChart needs to implement admin_view.")

    def teacher_view(self):
        raise NotImplementedError("Subclass of GroupDrivenChart needs to implement teacher_view.")


    def __init__(self, request):
        """
        Sets up the user and user_group for the View Driver, by examining the request
        """

        self.user = request.user
        self.user_group = self.user.userinfo.group.pk
        self.request = request

    def handle(self):
        """
        Calls the correct member view based on the group of the user who sent the request.
        """

        if self.user_group == HWCentralGroup.STUDENT:
            return self.student_view()
        elif self.user_group == HWCentralGroup.PARENT:
            return self.parent_view()
        elif self.user_group == HWCentralGroup.ADMIN:
            return self.admin_view()
        elif self.user_group == HWCentralGroup.TEACHER:
            return self.teacher_view()
        else:
            raise InvalidHWCentralGroupException(self.user.userinfo.group.name)


class StudentChartGet(GroupDrivenChart):
    def __init__(self, request, student_id):
        super(StudentChartGet, self).__init__(request)
        self.student = get_object_or_404(User, pk=student_id)
        if self.student.userinfo.group != HWCentralGroup.STUDENT:
            raise Http404

    def full_student_data(self):
        return JsonResponse(StudentPerformance(self.student))

    def student_view(self):
        # validation - only the logged in student should be able to see his/her own chart
        if self.student.pk != self.user.pk:
            return HttpResponseForbidden()

        return self.full_student_data()

    def parent_view(self):
        #validation - the logged in parent should only see the chart of his/her child
        if not self.user.home.students.filter(pk=self.student.pk).exists():
            return HttpResponseForbidden()

        return self.full_student_data()

    def admin_view(self):
        #validation - the logged in admin should only see the student chart if student belongs to same school
        if not self.user.userinfo.school == self.student.userinfo.school:
            return HttpResponseForbidden()

        return self.full_student_data()

    def teacher_view(self):
        #validation - the logged in classteacher should only see the student chart if student belongs to his/her class

        # first check if user is a classteacher
        if self.user.classes_managed_set.count() == 0:
            return HttpResponseForbidden()

        # check if student belongs to the set of classes
        if not (self.user.classes_managed_set.all() & self.student.classes_enrolled_set.all()).exists():
            return HttpResponseForbidden()

        return self.full_student_data()


class StudentSingleSubjectChartGet(GroupDrivenChart):
    def __init__(self, request, subjectroom_id, student_id):
        super(StudentSingleSubjectChartGet, self).__init__(request)
        self.student = get_object_or_404(User, pk=student_id)
        if self.student.userinfo.group != HWCentralGroup.STUDENT:
            raise Http404
        self.subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)

        # check if provided student belongs to the provided subjectroom
        try:
            self.subjectroom.students.all().get(pk=self.student.pk)
        except User.DoesNotExist:
            raise Http404


    def student_view(self):
        return HttpResponseForbidden()

    def parent_view(self):
        return HttpResponseForbidden()

    def admin_view(self):
        return HttpResponseForbidden()

    def teacher_view(self):
        #validation - the logged in subjectteacher should only see the student chart if student belongs to his/her subjectroom

        # first check if user is a subjectteacher
        if self.user.subjects_managed_set.count() == 0:
            return HttpResponseForbidden()

        # check if teacher is managing the given subjectroom
        try:
            self.user.subjects_managed_set.all().get(pk=self.subjectroom.pk)
        except SubjectRoom.DoesNotExist:
            return HttpResponseForbidden()

        return JsonResponse(PerformanceBreakdown(self.student, self.subjectroom))


class SubjectroomChartGet(GroupDrivenChart):
    def __init__(self, request, subjectroom_id):
        super(SubjectroomChartGet, self).__init__(request)
        self.subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
        if self.student.userinfo.group != HWCentralGroup.STUDENT:
            raise Http404

    def full_student_data(self):
        return JsonResponse(StudentPerformance(self.student))

    def student_view(self):
        # validation - only the logged in student should be able to see his/her own chart
        if self.student.pk != self.user.pk:
            return HttpResponseForbidden()

        return self.full_student_data()

    def parent_view(self):
        #validation - the logged in parent should only see the chart of his/her child
        if not self.user.home.students.filter(pk=self.student.pk).exists():
            return HttpResponseForbidden()

        return self.full_student_data()

    def admin_view(self):
        #validation - the logged in admin should only see the student chart if student belongs to same school
        if not self.user.userinfo.school == self.student.userinfo.school:
            return HttpResponseForbidden()

        return self.full_student_data()

    def teacher_view(self):
        #validation - the logged in classteacher should only see the student chart if student belongs to his/her class

        # first check if user is a classteacher
        if self.user.classes_managed_set.count() == 0:
            return HttpResponseForbidden()

        # check if student belongs to the set of classes
        if not (self.user.classes_managed_set.all() & self.student.classes_enrolled_set.all()).exists():
            return HttpResponseForbidden()

        return self.full_student_data()