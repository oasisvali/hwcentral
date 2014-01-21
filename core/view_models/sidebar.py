from core.models import ClassRoom
from core.modules.constants import HWCentralGroup
from core.routing.url_names import UrlNames
from hwcentral.exceptions import InvalidStateException


class Sidebar(object):
    def __init__(self, user):
        self.user_group = user.userinfo.group.name
        self.user_fullname = '%s %s' % (user.first_name, user.last_name)
        self.user_school = user.userinfo.school.name

        self.listing = SidebarListing(user, self.user_group)


class SidebarListingElement(object):
    """
    Just a container class to hold the label and the id (passed as a url param) for each Sidebar Listing Element
    """

    def __init__(self, label, id):
        self.label = label
        self.id = id


class SidebarListing(object):
    def __init__(self, user, user_group):

        # right now Teacher's sidebar listing is a bit different compared to the others
        if user_group == HWCentralGroup.TEACHER:
            raise NotImplementedError()
        else:
            if user_group == HWCentralGroup.PARENT:
                self.title = 'Students'
                self.url_name = UrlNames.STUDENT.name
                self.elements = self.get_students(user, user_group)
            elif user_group == HWCentralGroup.STUDENT:
                self.title = 'Subjects'
                self.url_name = UrlNames.SUBJECT.name
                self.elements = self.get_subjects(user, user_group)
            elif user_group == HWCentralGroup.ADMIN:
                self.title = 'Classrooms'
                self.url_name = UrlNames.CLASSROOM.name
                self.elements = self.get_classrooms(user, user_group)
            else:
                raise InvalidStateException('Invalid HWCentralGroup: %s' % user_group)

    def get_students(self, user, user_group):
        assert user_group == HWCentralGroup.PARENT

        students = user.home.students.all()
        # Just check that this parent's home was set up correctly
        assert len(students) > 0

        listing_elements = []
        for student in students:
            listing_elements += [
                SidebarListingElement('%s %s' % (student.first_name, student.last_name), student.username)]

        return listing_elements


    def get_subjects(self, user, user_group):
        assert user_group == HWCentralGroup.STUDENT

        subjects = user.subjects_enrolled_set.all()
        # Just check that this student's subjects were up correctly
        assert len(subjects) > 0

        listing_elements = []
        for subject in subjects:
            listing_elements += [SidebarListingElement(subject.subject, subject.pk)]

        return listing_elements

    def get_classrooms(self, user, user_group):
        assert user_group == HWCentralGroup.ADMIN

        classrooms = ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number', 'division')
        # Just check that this school's classrooms were set up correctly
        assert len(classrooms) > 0

        listing_elements = []
        for classroom in classrooms:
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements += [
                SidebarListingElement('%s - %s' % (classroom.standard.number, classroom.division), classroom.pk)]

        return listing_elements


class Teacher_SidebarListingGrouping(object):
    """
    Special class to be used when the User is a Teacher, because a Teacher's Sidebar listing is a bit more complicated
    """