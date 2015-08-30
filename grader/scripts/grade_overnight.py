# to use this script, run following command from the terminal
# python manage.py runscript scripts.grade_overnight -v3

# NOTE: it is to be run the night after while hwcentral is down (since it grades submissions that were due on the previous day)
from datetime import timedelta

import django
from django.db.models import Avg

from core.models import Assignment, Submission
from core.view_drivers.assignment_id import create_shell_submission
from grader import grader_api


def run():
    # get current datetime
    now = django.utils.timezone.now()

    # get yesterday
    yesterday = now - timedelta(days=1)

    assignments_graded = 0
    submissions_graded = 0
    shell_submissions_created = 0

    # loop thru all the assignments that need to be graded
    for closed_assignment in Assignment.objects.filter(due__gt=yesterday, due__lt=now):
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

        # update the database object with marks - assignment
        closed_assignment.average = Submission.objects.filter(assignment=closed_assignment).aggregate(Avg('marks'))[
            'marks__avg']
        closed_assignment.save()
        assignments_graded += 1

    print 'GRADING SUMMARY ->'
    print 'Assignments Graded:', assignments_graded
    print 'Submissions Graded:', submissions_graded
    print 'Shell Submissions Created:', shell_submissions_created
