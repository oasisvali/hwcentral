# to use this script, run following command from the terminal
# python manage.py runscript grade_overnight --script-args="#h"

# NOTE: it is to be run the night after while hwcentral is down (since it grades submissions that were due on the previous day)
import argparse
import traceback
from datetime import timedelta

import django
from django.core.mail import mail_admins
from django.db.models import Avg, Q

from core.models import Assignment, Submission
from core.view_drivers.assignment_id import create_shell_submission
from edge.edge_api import reset_edge_data, calculate_edge_data
from grader import grader_api
from scripts.email.hwcentral_users import runscript_args_workaround


def run(*args):
    parser = argparse.ArgumentParser(description="Grade a bunch of assignments that are due")
    parser.add_argument('--reset', '-r', action='store_true',
                        help='Grade all assignments past their due date, not just the ones due over the last day')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    try:
        report = run_actual(processed_args.reset)
    except:
        report = traceback.format_exc()

    print report
    mail_admins("Grader Report", report)


def run_actual(reset):
    # get current datetime
    now = django.utils.timezone.now()
    report = "GRADER Run on %s\n" % now

    # get yesterday
    yesterday = now - timedelta(days=1)

    assignments_graded = 0
    submissions_graded = 0
    shell_submissions_created = 0

    # loop thru all the assignments that need to be graded
    due_assignments_filter = Q(due__lt=now)
    if reset:
        # reset edge data if all the calculations are to be redone
        reset_edge_data()
    else:
        due_assignments_filter &= Q(due__gt=yesterday)

    for closed_assignment in Assignment.objects.filter(due_assignments_filter):
        # check if submission exists for each student in the assignment's subjectroom
        for student in closed_assignment.subjectRoom.students.all():
            try:
                submission = Submission.objects.get(student=student, assignment=closed_assignment)
            except Submission.DoesNotExist:
                submission = create_shell_submission(closed_assignment, student, closed_assignment.due)
                shell_submissions_created += 1

            # grade each submission individually using grader
            grader_api.grade(submission)
            submissions_graded += 1

        # update the database object with marks & completion - assignment
        closed_assignment.average = Submission.objects.filter(assignment=closed_assignment).aggregate(Avg('marks'))[
            'marks__avg']
        closed_assignment.completion = \
        Submission.objects.filter(assignment=closed_assignment).aggregate(Avg('completion'))[
            'completion__avg']
        closed_assignment.save()
        assignments_graded += 1

    report += 'Assignments Graded: %s\n' % assignments_graded
    report += 'Submissions Graded: %s\n' % submissions_graded
    report += 'Shell Submissions Created: %s\n' % shell_submissions_created

    try:
        calculate_edge_data()
        report += 'Edge data calculated successfully\n'
    except:
        report += 'Error while calculating edge data:\n%s\n' % traceback.format_exc()

    return report
