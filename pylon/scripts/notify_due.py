# to use this script, run following command from the terminal
# python manage.py runscript notify_due

# NOTE: it is to be run every day to notify parents and teachers about assignments due the next day
import traceback
from datetime import timedelta

import django
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models import Q

from core.models import Assignment
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils
from core.utils.teacher import TeacherUtils
from pylon.pylon_api import notify_due_parent, PylonApiError, notify_due_teacher


def run():
    # get current datetime
    now = django.utils.timezone.now()
    report = "PYLON Due Run on %s\n" % now

    try:
        report += "\nNotifying Parents ->\n"
        report += notify_due_parents()
    except:
        report += 'Error while notifying parents:\n%s\n' % traceback.format_exc()

    try:
        report += "\nNotifying Teachers ->\n"
        report += notify_due_teachers()
    except:
        report += 'Error while notifying teachers:\n%s\n' % traceback.format_exc()

    report += '\nTotal execution time: %s\n' % (django.utils.timezone.now() - now)

    print report
    mail_admins("Pylon Due Report", report)


def notify_due_parents():
    now = django.utils.timezone.now()
    tomorrow = now + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)

    report = ''
    total_notifications = 0
    successful_notifications = 0

    for parent in User.objects.filter(userinfo__group=HWCentralGroup.refs.PARENT):
        for child in parent.home.children.all():
            utils = StudentUtils(child)
            assignments = Assignment.objects.filter(
                (Q(subjectRoom__pk__in=utils.get_enrolled_subjectroom_ids()) | Q(
                    remedial__pk__in=utils.get_enrolled_remedial_ids()))
                & Q(due__gte=tomorrow) & Q(assigned__lte=now) & Q(due__lte=day_after)
            )
            if assignments.count() == 0:
                continue

            total_notifications += 1
            try:
                notify_due_parent(parent, child, assignments)
                successful_notifications += 1
            except PylonApiError as e:
                report += "%s\n" % e

    report += 'Total Notifications: %s\n' % total_notifications
    report += 'Successful Notifications: %s\n' % successful_notifications

    return report


def notify_due_teachers():
    now = django.utils.timezone.now()
    tomorrow = now + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)

    report = ''
    total_notifications = 0
    successful_notifications = 0

    for teacher in User.objects.filter(userinfo__group=HWCentralGroup.refs.TEACHER):
        utils = TeacherUtils(teacher)
        assignments = Assignment.objects.filter(
            (Q(subjectRoom__pk__in=utils.get_managed_subjectroom_ids()) | Q(
                remedial__focusRoom__pk__in=utils.get_managed_focusroom_ids()))
            & Q(due__gte=tomorrow) & Q(assigned__lte=now) & Q(due__lte=day_after)
        )

        if assignments.count() == 0:
            continue

        total_notifications += 1
        try:
            notify_due_teacher(teacher, assignments)
            successful_notifications += 1
        except PylonApiError as e:
            report += "%s\n" % e

    report = 'Total Notifications: %s\n' % total_notifications
    report += 'Successful Notifications: %s\n' % successful_notifications

    return report
