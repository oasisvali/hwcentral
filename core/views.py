from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from core.models import Assignment, SubjectRoom, ClassRoom, AssignmentQuestionsList, Submission
from core.routing.urlnames import UrlNames
from cabinet import cabinet
from cabinet.cabinet import ENCODING_SEPERATOR, SIGNER
from core.utils.constants import HWCentralAssignmentType
from core.utils.user_checks import check_subjectteacher, check_student
from core.view_drivers.announcement import AnnouncementGet, AnnouncementPost
from core.view_drivers.assignment_id import AssignmentIdGetInactive, AssignmentIdGetUncorrected
from core.view_drivers.assignment import AssignmentGet, AssignmentPost
from core.view_drivers.assignment_preview_id import AssignmentPreviewIdGet
from core.view_drivers.chart import SubjectroomChartGet, SingleSubjectStudentChartGet, \
    SubjectTeacherSubjectroomChartGet, ClassTeacherSubjectroomChartGet, AssignmentChartGet, StandardAssignmentChartGet, \
    get_assignment_type, is_assignment_corrected
from core.view_drivers.classroom_id import ClassroomIdGet
from core.view_drivers.chart import StudentChartGet
from core.view_drivers.home import HomeGet
from core.view_drivers.password import PasswordGet, PasswordPost
from core.view_drivers.settings import SettingsGet
from core.view_drivers.subject_id import SubjectIdGet




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
from hwcentral.exceptions import InvalidHWCentralAssignmentTypeException, InvalidStateException


def index_get(request):
    """
    View that handles requests to the base url. If user is logged in, redirect to home,
    otherwise render the index page
    """

    if request.user.is_authenticated():
        return redirect(UrlNames.HOME.name)

    # just display the index template
    return render(request, UrlNames.INDEX.get_template())


@login_required
def home_get(request):
    return HomeGet(request).handle()


@login_required
def settings_get(request):
    return SettingsGet(request).handle()


@login_required
def subject_id_get(request, subject_id):
    subject = get_object_or_404(SubjectRoom, pk=subject_id)
    return SubjectIdGet(request, subject).handle()


@login_required
def classroom_id_get(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    return ClassroomIdGet(request, classroom).handle()


@login_required
def assignment_get(request):
    return AssignmentGet(request).handle()


@login_required
def assignment_post(request):
    return AssignmentPost(request).handle()

@login_required
def assignment_override_get(request):
    return AssignmentGet(request, True).handle()


@login_required
def assignment_override_post(request):
    return AssignmentPost(request, True).handle()


@login_required
def assignment_preview_id_get(request, assignment_questions_list_id):
    assignment_questions_list = get_object_or_404(AssignmentQuestionsList, pk=assignment_questions_list_id)
    return AssignmentPreviewIdGet(request, assignment_questions_list).handle()


@login_required
def assignment_id_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # Assignment can be inactive, uncorrected or corrected
    assignment_type = get_assignment_type(assignment)

    if assignment_type == HWCentralAssignmentType.INACTIVE:
        return AssignmentIdGetInactive(request, assignment).handle()
    elif assignment_type == HWCentralAssignmentType.UNCORRECTED:
        return AssignmentIdGetUncorrected(request, assignment).handle()
    elif assignment_type == HWCentralAssignmentType.CORRECTED:
        return HttpResponseNotFound()  # Only submissions are viewed after an assignment has been corrected
    else:
        raise InvalidHWCentralAssignmentTypeException(assignment_type)


@login_required
def submission_id_get(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    assignment_type = get_assignment_type(submission.assignment)

    if assignment_type == HWCentralAssignmentType.INACTIVE:
        raise InvalidStateException("Submission %s for inactive assignment %s" % (submission, submission.assignment))
    elif assignment_type == HWCentralAssignmentType.UNCORRECTED:
        return SubmissionIdGetUncorrected(request, submission).handle()
    elif assignment_type == HWCentralAssignmentType.CORRECTED:
        return SubmissionIdGetCorrected(request, submission).handle()
    else:
        raise InvalidHWCentralAssignmentTypeException(assignment_type)


@login_required
def submission_id_post(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    # submissions can only be submitted for active, uncorrected assignments
    assignment_type = get_assignment_type(submission.assignment)

    if assignment_type != HWCentralAssignmentType.UNCORRECTED:
        raise Http404

    return SubmissionIdPostUncorrected(request, submission).handle()

@login_required
def student_chart_get(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    check_student(student)
    return StudentChartGet(request, student).handle()


@login_required
def single_subject_student_chart_get(request, student_id, subjectroom_id):
    student = get_object_or_404(User, pk=student_id)
    check_student(student)
    subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)

    # check if provided student belongs to the provided subjectroom
    try:
        subjectroom.students.get(pk=student.pk)
    except User.DoesNotExist:
        raise Http404

    return SingleSubjectStudentChartGet(request, subjectroom, student).handle()

@login_required
def subjectroom_chart_get(request, subjectroom_id):
    subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    return SubjectroomChartGet(request, subjectroom).handle()


@login_required
def subject_teacher_subjectroom_chart_get(request, subjectteacher_id):
    subjectteacher = get_object_or_404(User, pk=subjectteacher_id)
    check_subjectteacher(subjectteacher)
    return SubjectTeacherSubjectroomChartGet(request, subjectteacher).handle()


@login_required
def class_teacher_subjectroom_chart_get(request, classteacher_id, classroom_id):
    classteacher = get_object_or_404(User, pk=classteacher_id)
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    if classroom.classTeacher != classteacher:
        raise Http404
    return ClassTeacherSubjectroomChartGet(request, classteacher, classroom).handle()


@login_required
def assignment_chart_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # only allow for corrected assignments
    if not is_assignment_corrected(assignment):
        raise Http404
    return AssignmentChartGet(request, assignment).handle()

@login_required
def standard_assignment_chart_get(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # only allow for corrected assignments
    if not is_assignment_corrected(assignment):
        raise Http404
    return StandardAssignmentChartGet(request, assignment).handle()


@login_required
def announcement_post(request):
    return AnnouncementPost(request).handle()

@login_required
def announcement_get(request):
    return AnnouncementGet(request).handle()

@login_required
def password_get(request):
    return PasswordGet(request).handle()


@login_required
def password_post(request):
    return PasswordPost(request).handle()


@login_required
def secure_static_get(request, b64_string):
    # first we decode the signed id
    id_signed = urlsafe_base64_decode(b64_string)

    # then we unsign the id
    id_unsigned = SIGNER.unsign(id_signed)

    # validation
    username = id_unsigned.split(ENCODING_SEPERATOR)[0]
    if request.user.username != username:
        raise Http404
    resource_url = id_unsigned[len(username) + 1:]
    if request.user.userinfo.school.pk != long(cabinet.extract_school_id_from_resource_url(resource_url)):
        raise Http404

    # validation passed - send request to static resource server and relay the response
    return HttpResponse(cabinet.get_static_content(resource_url), content_type='image/jpeg')