from django.contrib.contenttypes.models import ContentType

from core.models import Announcement, School, ClassRoom, SubjectRoom
from core.utils.references import HWCentralGroup


def get_list_active_subject_assignments(user):
    """
    used to get total assignments in a subject for STUDENT related to given user PARENT. used in the parents view to
    obtain a 3D array for graph on the page. 3D array returned has elements: user_id, subject,incompleteassignments

    """

    assert user.userinfo.group == HWCentralGroup.refs.PARENT
    # incase parents have multiple kids then count the number of kids and then get the total list of active assignments
    # for individual kids
    listing = []  # A 3D array with columns : user_id (for the student),Subject,total incomplete assignments.
    element = []
    studentscore = None
    subject_element = []

    # if user.home.students.count() > 0:
    #
    # # for individual student in the list of the students you receive as the kids of the parents
    #     for student in user.home.students.all():
    #         # build a list of all assignments in given subject - T  ODO: this might be possible to do in a single query - use Q
    #         for subject in student.subjects_enrolled_set.all():
    #             subject_id = subject.pk
    #
    #             total_incomplete_assignment = len(get_list_unfinished_assignments_by_subject(student, subject_id))
    #             assignments = get_list_active_student_subject_assignments(student, subject)
    #             for assignment in assignments:
    #                 class_average = get_class_average_for_assignment(assignment)
    #                 if class_average == None:
    #                     class_average = 0
    #                 class_average = round(class_average, 2)
    #                 try:
    #                     submission = Submission.objects.get(assignment=assignment, student=student)
    #                     if submission.completion == 1:
    #                         studentscore = Submission.objects.get(student=student, assignment=assignment).marks
    #                 except Submission.DoesNotExist:
    #                     pass
    #                 element.append(
    #                     StudentGraphInfo(assignment, studentscore, class_average))
    #                 studentscore = None
    #         subject_element.append(SubjectListings(subject, element, total_incomplete_assignment))
    #     listing.append(UserListings(student,
    #                                 subject_element))  # return the count of total number of assignments along with related userID,subjects.
    return listing


def get_list_parent_announcements(user, limit=10, offset=0):
    """
    The list is sorted in most-recent to least-recent order
    @param user: The user for whom the relevant announcements are required
    """

    # right now only supporting student
    assert user.userinfo.group == HWCentralGroup.refs.PARENT

    announcements = []

    # get announcements for this school
    announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(School),
                                                     object_id=user.userinfo.school.pk))
    # get announcements for this class
    for classRoom in user.classes_enrolled_set.all():
        announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(ClassRoom),
                                                         object_id=classRoom.pk))
    # get announcements for all subjects
    for subject in user.subjects_enrolled_set.all():
        announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(SubjectRoom),
                                                         object_id=subject.pk))

    # sort and page
    return sorted(announcements, key=lambda announcement: announcement.timestamp, reverse=True)[offset:limit]