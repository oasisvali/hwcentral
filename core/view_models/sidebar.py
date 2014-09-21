from core.models import ClassRoom
from core.modules.constants import HWCentralGroup
from core.routing.url_names import UrlNames
from core.view_models.util import Link
from hwcentral.exceptions import InvalidStateException


class Sidebar(object):
    def __init__(self, user):
        self.user_group = user.userinfo.group.name
        self.user_fullname = '%s %s' % (user.first_name, user.last_name)
        self.user_school = user.userinfo.school.name

        self.school_urlname = UrlNames.SCHOOL.name
        self.settings_urlname = UrlNames.SETTINGS.name
        self.fullname_urlname = UrlNames.HOME.name

        self.listings = []

        # right now Teacher's sidebar listing is a bit different compared to the others
        if self.user_group == HWCentralGroup.TEACHER:
            self.listings = self.get_teacher_listings(user, self.user_group)
        else:
            if self.user_group == HWCentralGroup.PARENT:
                self.listings = [ParentSidebarListing(user, self.user_group)]
            elif self.user_group == HWCentralGroup.STUDENT:
                self.listings = [StudentSidebarListing(user, self.user_group)]
            elif self.user_group == HWCentralGroup.ADMIN:
                self.listings = [AdminSidebarListing(user, self.user_group)]
            else:
                raise InvalidStateException('Invalid HWCentralGroup: %s' % self.user_group)

    def get_teacher_listings(self, user, user_group):
        assert user_group == HWCentralGroup.TEACHER

        teacher_listings = []

        # first get list of all classrooms managed by this teacher. Create a classrooms listing only if this teacher is actually a class teacher for a classroom
        classrooms = user.classes_managed_set.all()
        if len(classrooms) > 0:
            classroom_listing_elements = []
            for classroom in classrooms:
                classroom_listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

            teacher_listings.append(SidebarListing("Classrooms", UrlNames.CLASSROOM.name, classroom_listing_elements))

        # now get list of all subject rooms taught by this teacher. Create a subject room listing only if this teacher actually teaches a subject
        subjects = user.subjects_managed_set.all()
        if len(subjects) > 0:
            subject_listing_elements = []
            for subject in subjects:
                subject_listing_elements.append(Link(subject.subject.name, subject.pk))

            teacher_listings.append(SidebarListing("Subjects", UrlNames.SUBJECT.name, subject_listing_elements))

        return teacher_listings


class SidebarListing(object):
    """
    Just a container class to hold listing information
    """

    def __init__(self, title, url_name, elements):
        self.title = title
        self.url_name = url_name
        self.elements = elements


class StudentSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(StudentSidebarListing, self).__init__('Subjects', UrlNames.SUBJECT.name,
                                                    self.get_subjects(user, user_group))

    def get_subjects(self, user, user_group):
        assert user_group == HWCentralGroup.STUDENT

        subjects = user.subjects_enrolled_set.all()
        # Just check that this student's subjects were up correctly
        assert len(subjects) > 0

        listing_elements = []
        for subject in subjects:
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ParentSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(ParentSidebarListing, self).__init__('Students', UrlNames.STUDENT.name,
                                                   self.get_students(user, user_group))

    def get_students(self, user, user_group):
        assert user_group == HWCentralGroup.PARENT

        students = user.home.students.all()
        # Just check that this parent's home was set up correctly
        assert len(students) > 0

        listing_elements = []
        for student in students:
            listing_elements.append(Link('%s %s' % (student.first_name, student.last_name), student.username))

        return listing_elements


class AdminSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(AdminSidebarListing, self).__init__('Classrooms', UrlNames.CLASSROOM.name,
                                                  self.get_classrooms(user, user_group))

    def get_classrooms(self, user, user_group):
        assert user_group == HWCentralGroup.ADMIN

        classrooms = ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number', 'division')
        # Just check that this school's classrooms were set up correctly
        assert len(classrooms) > 0

        listing_elements = []
        for classroom in classrooms:
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return listing_elements


def get_classroom_label(classroom):
    return '%s - %s' % (classroom.standard.number, classroom.division)