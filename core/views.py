from datadog import statsd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import mail_managers
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from cabinet import cabinet_api
from cabinet.cabinet_api import SIGNER, ENCODING_SEPERATOR
from concierge.forms import EnquirerForm
from core.models import Assignment, SubjectRoom, ClassRoom, AssignmentQuestionsList, Submission
from core.routing.urlnames import UrlNames
from core.utils.assignment import get_assignment_type, is_assignment_corrected
from core.utils.constants import HWCentralAssignmentType
from core.utils.json import Json404Response
from core.utils.references import HWCentralGroup
from core.utils.toast import render_with_success_toast, render_with_error_toast
from core.utils.user_checks import is_subjectroom_student_relationship, \
    is_subjectteacher
from core.view_drivers.announcement import AnnouncementGet, AnnouncementPost
from core.view_drivers.assignment_id import AssignmentIdGetInactive, AssignmentIdGetUncorrected
from core.view_drivers.assignment import AssignmentGet, AssignmentPost
from core.view_drivers.assignment_preview_id import AssignmentPreviewIdGet
from core.view_drivers.chart import SubjectroomChartGet, SingleSubjectStudentChartGet, \
    SubjectTeacherSubjectroomChartGet, ClassTeacherSubjectroomChartGet, AssignmentChartGet, StandardAssignmentChartGet
from core.view_drivers.classroom_id import ClassroomIdGet
from core.view_drivers.chart import StudentChartGet
from core.view_drivers.home import HomeGet
from core.view_drivers.password import PasswordGet, PasswordPost
from core.view_drivers.settings import SettingsGet
from core.view_drivers.subject_id import SubjectIdGet, ParentSubjectIdGet










# def render_register(request, user_creation_form, user_info_form):
# """
#     A helper to reduce code duplication between different register HTTP methods (get/post)
#     @param request:         The original request
#     @param user_creation_form:       newly created / validated UserCreationForm instance
#     @param user_info_form:  newly created / validated UserInfoForm instance
#     @return: HTTPResponse returned by the render method
#     """
#     return render(request, UrlNames.REGISTER.get_template(), {
#         'user_creation_form': user_creation_form,
#         'user_info_form': user_info_form
#     })
#
#
# def register_get(request):
#     return render_register(request, UserCreationForm(), UserInfoForm())
#
#
# def register_post(request):
#     user_creation_form = UserCreationForm(request.POST)
#     user_info_form = UserInfoForm(request.POST)
#     if user_creation_form.is_valid() and user_info_form.is_valid():
#         # save new user and bind the new user info to it
#         new_user = user_creation_form.save()
#         new_user_info = user_info_form.save(commit=False)
#         new_user_info.user = new_user
#         new_user_info.save()
#
#         # log user in
#         login(request, new_user)
#         return redirect(UrlNames.HOME.name)
#
#     # else if both forms are not valid
#     return render_register(request, user_creation_form, user_info_form)


# BUSINESS VIEWS
from core.view_drivers.submission_id import SubmissionIdGetUncorrected, SubmissionIdGetCorrected, \
    SubmissionIdPostUncorrected
from core.view_models.index import IndexViewModel
from hwcentral.exceptions import InvalidHWCentralAssignmentTypeError, InvalidStateError
from hwcentral.settings import LOGIN_REDIRECT_URL


def logout_wrapper(logout_view):
    """
    Redirects to index if already logged out, otherwise proceeds to logout
    """

    def delegate_logout(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(UrlNames.INDEX.name)
        statsd.increment('core.hits.logout')
        return logout_view(request, *args, **kwargs)

    return delegate_logout


def login_wrapper(login_view):
    """
    Redirects to settings.LOGIN_REDIRECT_URL if already logged in, otherwise proceeds to login
    """

    def delegate_login(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(LOGIN_REDIRECT_URL)
        statsd.increment('core.hits.login')
        return login_view(request, *args, **kwargs)

    return delegate_login


@statsd.timed('core.get.index')
def index_get(request):
    """
    View that handles requests to the base url. If user is logged in, redirect to home,
    otherwise render the index page
    """
    statsd.increment('core.hits.get.index')

    if request.user.is_authenticated():
        return redirect(UrlNames.HOME.name)

    # just display the index template
    return render(request, UrlNames.INDEX.get_template(), IndexViewModel(EnquirerForm()).as_context())


@statsd.timed('core.post.index')
def index_post(request):
    statsd.increment('core.hits.post.index')

    if request.user.is_authenticated():
        return redirect(UrlNames.HOME.name)

    index_form = EnquirerForm(request.POST)
    if index_form.is_valid():
        enquirer = index_form.save()
        mail_managers("Enquiry", enquirer.dump_to_email())
        return render_with_success_toast(request,
                                         'Your request has been recorded. The HWCentral team will reach out to you shortly.',
                                         UrlNames.INDEX.get_template(), IndexViewModel(EnquirerForm()).as_context())

    return render_with_error_toast(request,
                                   'There was a problem with your contact information. Please fix the errors and try again.',
                                   UrlNames.INDEX.get_template(), IndexViewModel(index_form).as_context())



@login_required
@statsd.timed('core.get.home')
def home_get(request):
    statsd.increment('core.hits.get.home')
    return HomeGet(request).handle()


@login_required
@statsd.timed('core.get.settings')
def settings_get(request):
    statsd.increment('core.hits.get.settings')
    return SettingsGet(request).handle()


@login_required
@statsd.timed('core.get.subject_id')
def subject_id_get(request, subject_id):
    statsd.increment('core.hits.get.subject_id')
    subjectroom = get_object_or_404(SubjectRoom, pk=subject_id)
    return SubjectIdGet(request, subjectroom).handle()


@login_required
@statsd.timed('core.get.parent_subject_id')
def parent_subject_id_get(request, subject_id, child_id):
    statsd.increment('core.hits.get.parent_subject_id')

    subjectroom = get_object_or_404(SubjectRoom, pk=subject_id)
    child = get_object_or_404(User, pk=child_id)

    if not is_subjectroom_student_relationship(subjectroom, child):
        raise Http404

    return ParentSubjectIdGet(request, subjectroom, child).handle()

@login_required
@statsd.timed('core.get.classroom_id')
def classroom_id_get(request, classroom_id):
    statsd.increment('core.hits.get.classroom_id')
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    return ClassroomIdGet(request, classroom).handle()


@login_required
@statsd.timed('core.get.assignment')
def assignment_get(request):
    statsd.increment('core.hits.get.assignment')
    return AssignmentGet(request).handle()


@login_required
@statsd.timed('core.post.assignment')
def assignment_post(request):
    statsd.increment('core.hits.post.assignment')
    return AssignmentPost(request).handle()

@login_required
@statsd.timed('core.get.assignment_override')
def assignment_override_get(request):
    statsd.increment('core.hits.get.assignment_override')
    return AssignmentGet(request, True).handle()


@login_required
@statsd.timed('core.post.assignment_override')
def assignment_override_post(request):
    statsd.increment('core.hits.post.assignment_override')
    return AssignmentPost(request, True).handle()


@login_required
@statsd.timed('core.get.assignment_preview_id')
def assignment_preview_id_get(request, assignment_questions_list_id):
    statsd.increment('core.hits.get.assignment_preview_id')
    assignment_questions_list = get_object_or_404(AssignmentQuestionsList, pk=assignment_questions_list_id)
    return AssignmentPreviewIdGet(request, assignment_questions_list).handle()


@login_required
@statsd.timed('core.get.assignment_id')
def assignment_id_get(request, assignment_id):
    statsd.increment('core.hits.get.assignment_id')

    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # Assignment can be inactive, uncorrected or corrected
    assignment_type = get_assignment_type(assignment)

    if assignment_type == HWCentralAssignmentType.INACTIVE:
        return AssignmentIdGetInactive(request, assignment).handle()
    elif assignment_type == HWCentralAssignmentType.UNCORRECTED:
        return AssignmentIdGetUncorrected(request, assignment).handle()
    elif assignment_type == HWCentralAssignmentType.CORRECTED:
        raise Http404  # Only submissions are viewed after an assignment has been corrected
    else:
        raise InvalidHWCentralAssignmentTypeError(assignment_type)


@login_required
@statsd.timed('core.get.submission_id')
def submission_id_get(request, submission_id):
    statsd.increment('core.hits.get.submission_id')

    submission = get_object_or_404(Submission, pk=submission_id)

    assignment_type = get_assignment_type(submission.assignment)

    if assignment_type == HWCentralAssignmentType.INACTIVE:
        raise InvalidStateError("Submission %s for inactive assignment %s" % (submission, submission.assignment))
    elif assignment_type == HWCentralAssignmentType.UNCORRECTED:
        return SubmissionIdGetUncorrected(request, submission).handle()
    elif assignment_type == HWCentralAssignmentType.CORRECTED:
        return SubmissionIdGetCorrected(request, submission).handle()
    else:
        raise InvalidHWCentralAssignmentTypeError(assignment_type)


@login_required
@statsd.timed('core.post.submission_id')
def submission_id_post(request, submission_id):
    statsd.increment('core.hits.post.submission_id')

    submission = get_object_or_404(Submission, pk=submission_id)

    # submissions can only be submitted for active, uncorrected assignments
    assignment_type = get_assignment_type(submission.assignment)

    if assignment_type != HWCentralAssignmentType.UNCORRECTED:
        raise Http404

    return SubmissionIdPostUncorrected(request, submission).handle()

@login_required
@statsd.timed('core.chart.student')
def student_chart_get(request, student_id):
    statsd.increment('core.hits.chart.student')

    try:
        student = get_object_or_404(User, pk=student_id)
    except Http404, e:
        return Json404Response(e)
    if student.userinfo.group != HWCentralGroup.refs.STUDENT:
        return Json404Response()

    return StudentChartGet(request, student).handle()


@login_required
@statsd.timed('core.chart.single_subject_student')
def single_subject_student_chart_get(request, student_id, subjectroom_id):
    statsd.increment('core.hits.chart.single_subject_student')

    try:
        student = get_object_or_404(User, pk=student_id)
    except Http404, e:
        return Json404Response(e)
    try:
        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    except Http404, e:
        return Json404Response(e)

    # check if provided student belongs to the provided subjectroom
    if not is_subjectroom_student_relationship(subjectroom, student):
        return Json404Response()

    return SingleSubjectStudentChartGet(request, subjectroom, student).handle()

@login_required
@statsd.timed('core.chart.subjectroom')
def subjectroom_chart_get(request, subjectroom_id):
    statsd.increment('core.hits.chart.subjectroom')
    try:
        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    except Http404, e:
        return Json404Response(e)
    return SubjectroomChartGet(request, subjectroom).handle()


@login_required
@statsd.timed('core.chart.subject_teacher_subjectroom')
def subject_teacher_subjectroom_chart_get(request, subjectteacher_id):
    statsd.increment('core.hits.chart.subject_teacher_subjectroom')

    try:
        subjectteacher = get_object_or_404(User, pk=subjectteacher_id)
    except Http404, e:
        return Json404Response(e)
    if not is_subjectteacher(subjectteacher):
        return Json404Response()

    return SubjectTeacherSubjectroomChartGet(request, subjectteacher).handle()


@login_required
@statsd.timed('core.chart.class_teacher_subjectroom')
def class_teacher_subjectroom_chart_get(request, classteacher_id, classroom_id):
    statsd.increment('core.hits.chart.class_teacher_subjectroom')
    try:
        classteacher = get_object_or_404(User, pk=classteacher_id)
    except Http404, e:
        return Json404Response(e)
    try:
        classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    except Http404, e:
        return Json404Response(e)
    if classroom.classTeacher != classteacher:
        return Json404Response()
    return ClassTeacherSubjectroomChartGet(request, classteacher, classroom).handle()


@login_required
@statsd.timed('core.chart.assignment')
def assignment_chart_get(request, assignment_id):
    statsd.increment('core.hits.chart.assignment')
    try:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
    except Http404, e:
        return Json404Response(e)
    # only allow for corrected assignments
    if not is_assignment_corrected(assignment):
        return Json404Response()
    return AssignmentChartGet(request, assignment).handle()

@login_required
@statsd.timed('core.chart.standard_assignment')
def standard_assignment_chart_get(request, assignment_id):
    statsd.increment('core.hits.chart.standard_assignment')
    try:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
    except Http404, e:
        return Json404Response(e)
    # only allow for corrected assignments
    if not is_assignment_corrected(assignment):
        return Json404Response()
    return StandardAssignmentChartGet(request, assignment).handle()


@login_required
@statsd.timed('core.post.announcement')
def announcement_post(request):
    statsd.increment('core.hits.post.announcement')
    return AnnouncementPost(request).handle()

@login_required
@statsd.timed('core.get.announcement')
def announcement_get(request):
    statsd.increment('core.hits.get.announcement')
    return AnnouncementGet(request).handle()

@login_required
@statsd.timed('core.get.password')
def password_get(request):
    statsd.increment('core.hits.get.password')
    return PasswordGet(request).handle()


@login_required
@statsd.timed('core.post.password')
def password_post(request):
    statsd.increment('core.hits.post.password')
    return PasswordPost(request).handle()


@login_required
@statsd.timed('core.get.secure_static')
def secure_static_get(request, b64_string):
    statsd.increment('core.hits.get.secure_static')

    # first we decode the signed id
    id_signed = urlsafe_base64_decode(b64_string)

    # then we unsign the id
    try:
        id_unsigned = SIGNER.unsign(id_signed)
    except BadSignature:
        raise Http404


    # validation
    username = id_unsigned.split(ENCODING_SEPERATOR)[0]
    if request.user.username != username:
        raise Http404

    # validation passed - send request to static resource server and relay the response
    resource_url = id_unsigned[len(username) + 1:]
    return HttpResponse(cabinet_api.get_static_content(resource_url), content_type='image/jpeg')

def test_500_get(request):
    """
    Used to test server error page
    """
    raise Exception('Testing 500 error page')
