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
from core.utils.assignment import check_homework_assignment
from core.utils.references import HWCentralGroup, HWCentralOpen
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
        if not parent.userinfo.school.schoolprofile.pylon:
            continue

        for child in parent.home.children.all():
            utils = StudentUtils(child)

            filter = Q(subjectRoom__pk__in=utils.get_enrolled_subjectroom_ids())
            if utils.focus:
                filter |= Q(remedial__pk__in=utils.get_enrolled_remedial_ids())

            assignments = Assignment.objects.filter(filter &
                                                    Q(due__gte=tomorrow) & Q(assigned__lte=now) & Q(due__lte=day_after)
            )
            if assignments.count() == 0:
                continue
            else:
                for assignment in assignments:
                    check_homework_assignment(assignment)

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
        if not teacher.userinfo.school.schoolprofile.pylon:
            continue

        if teacher.userinfo.school == HWCentralOpen.refs.SCHOOL:
            continue

        utils = TeacherUtils(teacher)

        filter = Q(subjectRoom__pk__in=utils.get_managed_subjectroom_ids())
        if utils.focus:
            filter |= Q(remedial__focusRoom__pk__in=utils.get_managed_focusroom_ids())

        assignments = Assignment.objects.filter(filter &
                                                Q(due__gte=tomorrow) & Q(assigned__lte=now) & Q(due__lte=day_after)
        )

        if assignments.count() == 0:
            continue
        else:
            for assignment in assignments:
                check_homework_assignment(assignment)

        total_notifications += 1
        try:
            notify_due_teacher(teacher, assignments)
            successful_notifications += 1
        except PylonApiError as e:
            report += "%s\n" % e

    report = 'Total Notifications: %s\n' % total_notifications
    report += 'Successful Notifications: %s\n' % successful_notifications

    return report
