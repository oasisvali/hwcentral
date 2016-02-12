# to use this script, run following command from the terminal
# python manage.py runscript grade_overnight --script-args="#h"

# NOTE: it is to be run the night after while hwcentral is down (since it grades submissions that were due on the previous day)
import argparse
import traceback
from datetime import timedelta

import django
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_admins
from django.db.models import Avg, Q

from core.models import Assignment, Submission, SubjectRoom
from core.view_drivers.assignment_id import create_shell_submission
from edge.edge_api import reset_edge_data, calculate_edge_data
from focus.models import Remedial
from grader import grader_api
from hwcentral.exceptions import InvalidContentTypeError, InvalidStateError
from pylon.scripts import notify_overnight
from scripts.email.hwcentral_users import runscript_args_workaround


def run(*args):
    parser = argparse.ArgumentParser(description="Grade a bunch of assignments that are due")
    parser.add_argument('--reset', '-r', action='store_true',
                        help='Grade all assignments past their due date, not just the ones due over the last day')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    success = run_actual(processed_args.reset)

    if (not processed_args.reset) and success:
        notify_overnight.run()


def run_actual(reset):
    # get current datetime
    now = django.utils.timezone.now()
    report = "GRADER Run on %s\n" % now

    if reset:
        # reset edge data if all the calculations are to be redone
        reset_edge_data()

    success = False
    try:
        report += handle_assignments(reset)
        try:
            report += calculate_edge_data()
            success = True
        except:
            report += '\nError while calculating edge data:\n%s\n' % traceback.format_exc()
    except:
        report += 'Error while handling closed assignments:\n%s\n' % traceback.format_exc()
        report += 'Skipping calculating edge data\n'

    report += '\nTotal execution time: %s\n' % (django.utils.timezone.now() - now)

    print report
    mail_admins("Grader Report", report)

    return success


def check_correct_assignment_type(assignment):
    if assignment.content_type == ContentType.objects.get_for_model(User):
        raise InvalidStateError("Practice assignment should not be filtered as a closed assignment for grader.")
    elif (assignment.content_type != ContentType.objects.get_for_model(Remedial)) and (
                assignment.content_type != ContentType.objects.get_for_model(SubjectRoom)):
        raise InvalidContentTypeError(assignment.content_type)


def handle_assignments(reset):
    assignments_graded = 0
    submissions_graded = 0
    shell_submissions_created = 0
    remedials_created = 0

    # build filter for assignments that need to be graded
    now = django.utils.timezone.now()
    due_assignments_filter = Q(due__lt=now) & (~Q(content_type=ContentType.objects.get_for_model(User)))
    if not reset:
        yesterday = now - timedelta(days=1)
        due_assignments_filter &= Q(due__gt=yesterday)


    for closed_assignment in Assignment.objects.filter(due_assignments_filter):

        # assert - can remove this in future
        check_correct_assignment_type(closed_assignment)

        students = closed_assignment.content_object.students.all()
        # check if submission exists for each student in the assignment's target student set
        for student in students:
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

        now = django.utils.timezone.now()

        # only do remedials if:
        # assignment is for subjectroom
        # reset is not being done
        # school has activated remedial

        if (
                        (closed_assignment.content_type == ContentType.objects.get_for_model(SubjectRoom)) and
                        (not reset) and
                    ((closed_assignment.get_subjectroom()).classRoom.school.schoolprofile.focusRoom)
        ):
            # create a remedial for the subjectroom of this closed assignment (if required)
            remedial_submissions = Submission.objects.filter(assignment=closed_assignment, marks__lt=0.3)
            if remedial_submissions.count() > 0:
                remedial = Remedial(focusRoom=(closed_assignment.get_subjectroom()).focusroom)
                remedial.save()
                for remedial_submission in remedial_submissions:
                    remedial.students.add(remedial_submission.student)
                remedial.save()
                # finally, create the new assignment and associate it with the remedial
                remedial_assignment = Assignment.objects.create(content_object=remedial,
                                                                assignmentQuestionsList=closed_assignment.assignmentQuestionsList,
                                                                assigned=closed_assignment.due,
                                                                number=Assignment.get_new_assignment_number(
                                                                    closed_assignment.assignmentQuestionsList,
                                                                        closed_assignment.get_subjectroom()),
                                                                due=closed_assignment.due + timedelta(days=3))
                remedials_created += 1

    report = 'Assignments Graded: %s\n' % assignments_graded
    report += 'Submissions Graded: %s\n' % submissions_graded
    report += 'Shell Submissions Created: %s\n' % shell_submissions_created
    report += 'Remedials Created: %s\n' % remedials_created

    return report