__author__ = 'hrishikesh'

from core.models import Submission
from core.utils.constants import HWCentralGroup
from core.utils.student import get_list_active_assignments


def get_list_active_subject_assignments(user):
    """
    used to get total assignments in a subject for STUDENT related to given user PARENT. used in the parents view to
    obtain a 3D array for graph on the page. 3D array returned has elements: user_id, subject,incompleteassignments

    """

    assert user.userinfo.group.pk == HWCentralGroup.PARENT
    # incase parents have multiple kids then count the number of kids and then get the total list of active assignments
    # for individual kids
    user_listings = []  # A 3D array with columns : user_id (for the student),Subject,total incomplete assignments.

    if user.home.students.count() > 0:
        # for individual student in the list of the students you receive as the kids of the parents
        for student in user.home.students.all():
            for subject in student.subjects_enrolled_set.all():
                # build a list of all assignments in given subject - T  ODO: this might be possible to do in a single query - use Q
                assignments = get_list_active_assignments(student)
                total_incomplete_assignment = 0
                for assignment, in assignments:
                    if Submission.objects.get(assignment=assignment, student=student).completion != 1:
                        total_incomplete_assignment += 1

                user_listings = user_listings.append(student.userinfo.user_id, subject, total_incomplete_assignment)
                # return the count of total number of assignments along with related userID,subjects.
        return user_listings
