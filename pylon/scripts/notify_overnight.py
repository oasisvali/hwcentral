# to use this script, run following command from the terminal
# python manage.py runscript notify_overnight

# NOTE: it is to be run the night after while hwcentral is down (since it notifies about assignments that were due on the previous day)
import traceback
from datetime import timedelta

import django
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_admins
from django.db.models import Q

from core.models import Assignment, Submission, SubjectRoom
from core.utils.references import HWCentralGroup
from core.utils.teacher import TeacherUtils
from focus.models import Remedial
from hwcentral.exceptions import InvalidContentTypeError, InvalidStateError
from pylon.pylon_api import notify_results_parent, PylonApiError, notify_results_teacher


def run():
    # get current datetime
    now = django.utils.timezone.now()
    report = "PYLON Results Run on %s\n" % now

    try:
        report += "\nNotifying Parents ->\n"
        report += notify_results_parents()
    except:
        report += 'Error while notifying parents:\n%s\n' % traceback.format_exc()

    try:
        report += "\nNotifying Teachers ->\n"
        report += notify_results_teachers()
    except:
        report += 'Error while notifying teachers:\n%s\n' % traceback.format_exc()

    report += '\nTotal execution time: %s\n' % (django.utils.timezone.now() - now)

    print report
    mail_admins("Pylon Results Report", report)


def check_correct_assignment_type(assignment):
    if assignment.content_type == ContentType.objects.get_for_model(User):
        raise InvalidStateError("Practice assignment should not be filtered as a closed assignment for grader.")
    elif (assignment.content_type != ContentType.objects.get_for_model(Remedial)) and (
                assignment.content_type != ContentType.objects.get_for_model(SubjectRoom)):
        raise InvalidContentTypeError(assignment.content_type)


def notify_results_parents():
    now = django.utils.timezone.now()
    yesterday = now - timedelta(days=1)

    report = ''
    total_notifications = 0
    successful_notifications = 0

    for parent in User.objects.filter(userinfo__group=HWCentralGroup.refs.PARENT):
        for child in parent.home.children.all():
            recent_submissions = Submission.objects.filter(
                Q(student=child) & Q(assignment__due__lte=now) & Q(assignment__due__gte=yesterday) & (
                ~Q(assignment__content_type=ContentType.objects.get_for_model(User))))
            if recent_submissions.count() == 0:
                continue

            total_notifications += 1
            try:
                notify_results_parent(parent, child, recent_submissions)
                successful_notifications += 1
            except PylonApiError as e:
                report += "%s\n" % e

    report = '\nTotal Notifications: %s\n' % total_notifications
    report += '\nSuccessful Notifications: %s\n' % successful_notifications

    return report


def notify_results_teachers():
    now = django.utils.timezone.now()
    yesterday = now - timedelta(days=1)

    report = ''
    total_notifications = 0
    successful_notifications = 0

    for teacher in User.objects.filter(userinfo__group=HWCentralGroup.refs.TEACHER):
        utils = TeacherUtils(teacher)
        assignments = Assignment.objects.filter(
            (Q(subjectRoom__pk__in=utils.get_managed_subjectroom_ids()) | Q(
                remedial__focusRoom__pk__in=utils.get_managed_focusroom_ids()))
            & Q(due__lte=now) & Q(due__gte=yesterday)
        )

        if assignments.count() == 0:
            continue

        total_notifications += 1
        try:
            notify_results_teacher(teacher, assignments)
            successful_notifications += 1
        except PylonApiError as e:
            report += "%s\n" % e

    report = '\nTotal Notifications: %s\n' % total_notifications
    report += '\nSuccessful Notifications: %s\n' % successful_notifications

    return report
