import os
from datetime import timedelta

import django
import plivo
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse

from core.models import SubjectRoom
from core.routing.urlnames import UrlNames
from core.utils.constants import HWCentralEnv
from core.utils.labels import get_user_label, get_percentage_label, get_subjectroom_label, get_focusroom_label
from core.utils.student import get_active_assignment_completion
from core.utils.teacher import get_uncorrected_assignment_completion_avg
from core.utils.user_checks import is_student_assignment_relationship
from focus.models import Remedial
from hwcentral.exceptions import InvalidStateError, InvalidContentTypeError
from hwcentral.settings import ENVIRON, HWCENTRAL_CONFIG_ROOT

SRC_PHONE = '917057216343'


class InvalidPhoneError(InvalidStateError):
    def __init__(self, user, phone, *args, **kwargs):
        super(InvalidPhoneError, self).__init__("Invalid phone number for Pylon: %s for user %s" % (phone, user))


class PylonApiError(InvalidStateError):
    def __init__(self, params, response, *args, **kwargs):
        super(PylonApiError, self).__init__("PylonApiError - Unexpected response code: %s - %s for params %s" % (
        response[0], response[1]['message'], params))


class DummyPylonApi(object):
    def send_message(self, params):
        mail_admins('HWCentral Sandbox SMS', str(params))
        return (202, {'message': 'message(s) queued'})


if ENVIRON == HWCentralEnv.PROD:
    with open(os.path.join(HWCENTRAL_CONFIG_ROOT, 'plivo_auth.txt'), 'r') as f:
        PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN = f.read().strip().split('\n')
    PYLON_API = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
else:
    PYLON_API = DummyPylonApi()


def send_sms(user, message):
    params = {
        'src': SRC_PHONE,
        'dst': user.dossier.get_sanitized_phone(),
        'text': message
    }

    response = PYLON_API.send_message(params)

    if response[0] != 202:
        raise PylonApiError(params, response)


def notify_due_parent(parent, child, assignments):
    send_sms(parent, build_message_due_parent(child, assignments))


def notify_results_parent(parent, child, submissions):
    send_sms(parent, build_message_results_parent(child, submissions))


def notify_due_teacher(teacher, assignments):
    send_sms(teacher, build_message_due_teacher(teacher, assignments))


def notify_results_teacher(teacher, assignments):
    send_sms(teacher, build_message_results_teacher(teacher, assignments))


def notify_activate(parent, password):
    send_sms(parent, build_message_activate(parent, password))


MESSAGE_PREFIX = 'Homework Central update: %s.'


def truncate_assignment_title(assignment):
    title = assignment.assignmentQuestionsList.chapter.name
    if len(title) > 20:
        return title[:20].strip()

    long_title = assignment.assignmentQuestionsList.get_title()
    if len(long_title) > 20:
        return title

    title = long_title
    long_title = assignment.get_title()
    if len(long_title) > 20:
        return title

    return long_title


def is_assignment_due_tomorrow(assignment):
    now = django.utils.timezone.now()
    return (now + timedelta(days=1)) < assignment.due < (now + timedelta(days=2))


def is_assignment_due_yesterday(assignment):
    now = django.utils.timezone.now()
    return (now - timedelta(days=1)) < assignment.due < now


def get_assignment_target_label(assignment):
    if assignment.content_type == ContentType.objects.get_for_model(SubjectRoom):
        return get_subjectroom_label(assignment.get_subjectroom())
    elif assignment.content_type == ContentType.objects.get_for_model(Remedial):
        return get_focusroom_label(get_subjectroom_label(assignment.get_subjectroom()))
    else:
        raise InvalidContentTypeError(assignment.content_type)


def build_message_due_parent(student, assignments):
    msg = [MESSAGE_PREFIX % get_user_label(student), 'Due at 10pm tomorrow:']
    for assignment in assignments:
        assert is_student_assignment_relationship(student, assignment)
        assert is_assignment_due_tomorrow(assignment)

        completion = get_percentage_label(get_active_assignment_completion(student, assignment))
        msg.append('%s -> %s completion.' % (truncate_assignment_title(assignment), completion))

    return ' '.join(msg)


def build_message_due_teacher(teacher, assignments):
    msg = [MESSAGE_PREFIX % get_user_label(teacher), 'Due at 10pm tomorrow:']
    for assignment in assignments:
        assert (assignment.get_subjectroom()).teacher == teacher
        assert is_assignment_due_tomorrow(assignment)

        completion = get_percentage_label(get_uncorrected_assignment_completion_avg(assignment)[1])
        target = get_assignment_target_label(assignment)
        msg.append('%s:%s -> %s completion.' % (target, truncate_assignment_title(assignment), completion))

    return ' '.join(msg)


def build_message_results_parent(student, submissions):
    msg = [MESSAGE_PREFIX % get_user_label(student), 'Today\'s results:']
    for submission in submissions:
        assert student == submission.student
        assert is_assignment_due_yesterday(submission.assignment)

        completion = get_percentage_label(submission.completion)
        marks = get_percentage_label(submission.marks)

        msg.append(
            '%s -> %s completion, %s correct.' % (truncate_assignment_title(submission.assignment), completion, marks))

    return ' '.join(msg)


def build_message_results_teacher(teacher, assignments):
    msg = [MESSAGE_PREFIX % get_user_label(teacher), 'Today\'s results:']
    for assignment in assignments:
        assert (assignment.get_subjectroom()).teacher == teacher
        assert is_assignment_due_yesterday(assignment)

        completion = get_percentage_label(assignment.completion)
        average = get_percentage_label(assignment.average)
        target = get_assignment_target_label(assignment)

        msg.append('%s:%s -> %s completion, %s average.' % (
        target, truncate_assignment_title(assignment), completion, average))

    return ' '.join(msg)


def build_message_activate(parent, password):
    msg = [
        'Welcome to Homework Central.',
        'Username - %s, Password - %s.' % (parent.username, password),
        'Login at http://%s%s.' % (Site.objects.get_current().domain, reverse(UrlNames.LOGIN.name)),
        'For support call 7057216343.'
    ]

    return ' '.join(msg)
