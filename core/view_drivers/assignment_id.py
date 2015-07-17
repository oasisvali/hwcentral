import django
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

from core.models import Submission
from core.routing.urlnames import UrlNames
from core.utils import cabinet
from core.view_drivers.assignment_preview_id import render_readonly_assignment
from core.view_drivers.base import GroupDriven
from core.view_drivers.chart import is_subjectroom_classteacher_relationship, is_student_assignment_relationship
from core.view_models.sidebar import TeacherSidebar, AdminSidebar, ParentSidebar
from croupier import croupier
from hwcentral.exceptions import InvalidStateException


class AssignmentIdGet(GroupDriven):
    def __init__(self, request, assignment):
        super(AssignmentIdGet, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.assignment = assignment


class AssignmentIdGetInactive(AssignmentIdGet):

    def student_endpoint(self):
        return HttpResponseNotFound()
    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        # admin can only see this inactive assignment if it belongs to his/her school
        if self.assignment.subjectRoom.classRoom.school != self.user.userinfo.school:
            return HttpResponseNotFound()
        return render_readonly_assignment(self.request, self.user, AdminSidebar(self.user),
                                          self.assignment.assignmentQuestionsList)

    def teacher_endpoint(self):
        # teacher can only see this inactive assignment if it was created by them or if it belongs to their classroom
        if not is_subjectroom_classteacher_relationship(self.assignment.subjectRoom, self.user):
            return HttpResponseNotFound()

        if self.assignment.subjectRoom.teacher != self.user:
            return HttpResponseNotFound()

        return render_readonly_assignment(self.request, self.user, TeacherSidebar(self.user),
                                          self.assignment.assignmentQuestionsList)


def create_shell_submission(user, assignment):
    """
    Creates shell submission both in database and in the cabinet
    """
    shell_submission_db = Submission.objects.create(assignment=assignment, student=user,
                                                    timestamp=django.utils.timezone.now(),
                              completion=0.0)
    # first we grab the question data to build the assignment from the cabinet
    questions = cabinet.build_assignment(user, assignment.assignmentQuestionsList)

    # then we use croupier to randomize the order
    questions_randomized = croupier.shuffle_for_time(questions)

    # then we use croupier to deal the values
    questions_randomized_dealt = croupier.deal_for_time(questions_randomized)

    cabinet.build_submission(shell_submission_db, questions_randomized_dealt)

    return shell_submission_db


class AssignmentIdGetUncorrected(AssignmentIdGet):
    def student_endpoint(self):
        # student can only see this assignment if he/she belongs to the subjectroom the assignment is for
        if not is_student_assignment_relationship(self.user, self.assignment):
            return HttpResponseNotFound()

        # check if a submission already exists for this user for this assignment. if it exists, just redirect to that active submission
        try:
            submission = Submission.objects.get(student=self.user, assignment=self.assignment)
            return redirect(UrlNames.SUBMISSION_ID.name, submission.pk)
        except MultipleObjectsReturned:
            raise InvalidStateException(
                'Multiple submissions for user %s for assignment %s' % (self.user, self.assignment))
        except Submission.DoesNotExist:
            # generate shell submission and redirect
            shell_submission_db = create_shell_submission(self.user, self.assignment)
            return redirect(UrlNames.SUBMISSION_ID.name, shell_submission_db.pk)


    def parent_endpoint(self):
        # parent can only see this assignment if it is assigned to one of their children
        for child in self.user.home.students.all():
            if is_student_assignment_relationship(child, self.assignment):
                return render_readonly_assignment(self.request, self.user, ParentSidebar(self.user),
                                                  self.assignment.assignmentQuestionsList)

        return HttpResponseNotFound()

    def admin_endpoint(self):
        # admin can only see this uncorrected assignment if it belongs to his/her school
        if self.assignment.subjectRoom.classRoom.school != self.user.userinfo.school:
            return HttpResponseNotFound()
        return render_readonly_assignment(self.request, self.user, AdminSidebar(self.user),
                                          self.assignment.assignmentQuestionsList)

    def teacher_endpoint(self):
        # teacher can only see this uncorrected assignment if it was created by them or if it belongs to their classroom
        if not is_subjectroom_classteacher_relationship(self.assignment.subjectRoom, self.user):
            return HttpResponseNotFound()

        if self.assignment.subjectRoom.teacher != self.user:
            return HttpResponseNotFound()

        return render_readonly_assignment(self.request, self.user, TeacherSidebar(self.user),
                                          self.assignment.assignmentQuestionsList)
