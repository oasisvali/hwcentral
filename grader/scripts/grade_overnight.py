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
from core.utils.assignment import is_corrected_open_assignment
from core.utils.references import HWCentralGroup
from core.view_drivers.assignment_id import create_shell_submission
from edge.edge_api import reset_edge_data, calculate_edge_data
from focus.models import Remedial
from grader import grader_api
from pylon.scripts import notify_overnight
from pylon.scripts.notify_overnight import check_homework_assignment
from scripts.email.hwcentral_users import runscript_args_workaround


def run(*args):
    parser = argparse.ArgumentParser(description="Grade the assignments that are due")
    parser.add_argument('--reset', '-r', action='store_true',
                        help='Grade all assignments past their due date, not just the ones due over the last day')
    # Notification can be done while running complete reset because the notification are sent only for overnight grading results
    parser.add_argument('--notify', '-n', action='store_true',
                        help='Notify parents and teachers about the results of the grader run')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    success = run_actual(processed_args.reset)

    if success:
        # only notify if grading is successful
        if (not processed_args.reset) or processed_args.notify:
            # notify if it is not a reset run or if the notify flag is set explicitly
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


def handle_assignments(reset):
    assignments_graded = 0
    submissions_graded = 0
    shell_submissions_created = 0
    remedials_created = 0

    # build filter for assignments that need to be graded
    now = django.utils.timezone.now()
    past_hw_filter = Q(due__lt=now) & (~Q(content_type=ContentType.objects.get_for_model(User)))
    if reset:
        # if reset is being done, then all practice assignments for open model should also be recorrected
        open_student_set = User.objects.filter(userinfo__group=HWCentralGroup.refs.OPEN_STUDENT)

        assignments_filter = past_hw_filter | (
            Q(content_type=ContentType.objects.get_for_model(User)) &
            Q(average__isnull=False) &
            Q(object_id__in=open_student_set)
        )

    else:
        yesterday = now - timedelta(days=1)
        assignments_filter = past_hw_filter & Q(due__gt=yesterday)

    for assignment in Assignment.objects.filter(assignments_filter):

        if is_corrected_open_assignment(assignment):
            # open assignments should only be graded by this script if reset is being done
            assert reset
            #  grade the submission
            grader_api.grade(Submission.objects.get(assignment=assignment), True)
            submissions_graded += 1

        else:
            check_homework_assignment(assignment)

            students = assignment.content_object.students.all()
            # check if submission exists for each student in the assignment's target student set
            for student in students:
                try:
                    submission = Submission.objects.get(student=student, assignment=assignment)
                except Submission.DoesNotExist:
                    submission = create_shell_submission(assignment, student, assignment.due)
                    shell_submissions_created += 1

                # grade each submission individually using grader
                grader_api.grade(submission, True)
                submissions_graded += 1

        # update the database object with marks & completion - assignment
        assignment.average = Submission.objects.filter(assignment=assignment).aggregate(Avg('marks'))[
            'marks__avg']
        assignment.completion = \
            Submission.objects.filter(assignment=assignment).aggregate(Avg('completion'))[
            'completion__avg']
        assignment.save()
        assignments_graded += 1

        # only create remedials if:
        # assignment is for subjectroom
        # reset is not being done
        # school has activated remedial

        if (
                        (assignment.content_type == ContentType.objects.get_for_model(SubjectRoom)) and
                        (not reset) and
                    ((assignment.get_subjectroom()).classRoom.school.schoolprofile.focus)
        ):
            # create a remedial for the subjectroom of this closed assignment (if required)
            remedial_submissions = Submission.objects.filter(assignment=assignment, marks__lt=0.3)
            if remedial_submissions.count() > 0:
                remedial = Remedial(focusRoom=(assignment.get_subjectroom()).focusroom)
                remedial.save()
                for remedial_submission in remedial_submissions:
                    remedial.students.add(remedial_submission.student)
                remedial.save()
                # finally, create the new assignment and associate it with the remedial
                remedial_assignment = Assignment.objects.create(content_object=remedial,
                                                                assignmentQuestionsList=assignment.assignmentQuestionsList,
                                                                assigned=assignment.due,
                                                                number=Assignment.get_new_assignment_number(
                                                                    assignment.assignmentQuestionsList,
                                                                    assignment.get_subjectroom()),
                                                                due=assignment.due + timedelta(days=3))
                remedials_created += 1

    report = 'Assignments Graded: %s\n' % assignments_graded
    report += 'Submissions Graded: %s\n' % submissions_graded
    report += 'Shell Submissions Created: %s\n' % shell_submissions_created
    report += 'Remedials Created: %s\n' % remedials_created

    return report