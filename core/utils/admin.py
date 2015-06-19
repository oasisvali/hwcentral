from django.contrib.contenttypes.models import ContentType

from core.utils.constants import HWCentralGroup
from core.models import Announcement, School, ClassRoom, SubjectRoom

"""
Contains functions for the content in the admin page

"""


def get_admin_school(user):
    """
    Returns the school of the admin
    :param user: admin user
    :return:school of the user
    """

    school = School.objects.filter(admin=user, board=None)
    return school


def get_admin_class_list(user):
    """
    Returns details of all the listed classes under the admin school
    :param user: admin user
    :return:school list containing details of classes of the admin's school
    """
    standard_list = []
    school_lister = []
    assert user.userinfo.group.pk == HWCentralGroup.ADMIN
    school = get_admin_school(user)
    standard_list = ClassRoom.objects.all()
    for school in standard_list:
        school_lister.append(school)
    return school_lister


def get_list_admin_announcements(user, limit=10, offset=0):
    """
    The list is sorted in most-recent to least-recent order
    @param user: The user for whom the relevant announcements are required
    """

    # right now only supporting student
    assert user.userinfo.group.pk == HWCentralGroup.ADMIN

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