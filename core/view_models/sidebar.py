from core.models import ClassRoom
from core.routing.urlnames import UrlNames
from core.view_models.util import Link


class Sidebar(object):
    def __init__(self, user, listings, ticker=None):
        self.user_group = user.userinfo.group.pk
        self.user_groupname = user.userinfo.group.name
        self.user_fullname = '%s %s' % (user.first_name, user.last_name)
        self.user_school = user.userinfo.school.name
        self.ticker = ticker

        self.school_urlname = UrlNames.SCHOOL.name
        self.fullname_urlname = UrlNames.HOME.name

        self.listings = listings


class Ticker(object):
    """
    Container class to hold a generic ticker
    """

    def __init__(self, label, urlname, value):
        self.label = label
        self.urlname = urlname
        self.value = value


class SidebarListing(object):
    """
    Just a container class to hold listing information
    """

    def __init__(self, title, urlname, elements):
        self.title = title
        self.urlname = urlname
        self.elements = elements


class TeacherClassroomsSidebarListing(SidebarListing):
    def __init__(self, user):
        super(TeacherClassroomsSidebarListing, self).__init__('Classrooms', UrlNames.CLASSROOM.name,
                                                              self.get_classroom_listing_elements(user))

    def get_classroom_listing_elements(self, user):
        classroom_listing_elements = []
        for classroom in user.classes_managed_set.all():
            classroom_listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return classroom_listing_elements


class TeacherSubjectsSidebarListing(SidebarListing):
    def __init__(self, user):
        super(TeacherSubjectsSidebarListing, self).__init__('Subjects', UrlNames.SUBJECT.name,
                                                            self.get_subject_listing_elements(user))

    def get_subject_listing_elements(self, user):
        subject_listing_elements = []
        for subject in user.subjects_managed_set.all():
            subject_listing_elements.append(Link('%s : %s - %s' % (subject.subject.name, subject.classRoom.standard,
                                                                   subject.classRoom.division), subject.pk))

        return subject_listing_elements


class StudentSidebarListing(SidebarListing):
    def __init__(self, user):
        super(StudentSidebarListing, self).__init__('Subjects', UrlNames.SUBJECT.name,
                                                    self.get_subjects(user))

    def get_subjects(self, user):
        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ParentSidebarListing(SidebarListing):
    def __init__(self, user):
        super(ParentSidebarListing, self).__init__('Students', UrlNames.STUDENT.name,
                                                   self.get_students(user))

    def get_students(self, user):
        listing_elements = []
        for student in user.home.students.all():
            listing_elements.append(Link('%s %s' % (student.first_name, student.last_name), student.username))

        return listing_elements


class AdminSidebarListing(SidebarListing):
    def __init__(self, user):
        super(AdminSidebarListing, self).__init__('Classrooms', UrlNames.CLASSROOM.name,
                                                  self.get_classrooms(user))

    def get_classrooms(self, user):
        listing_elements = []
        for classroom in ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number',
                                                                                        'division'):
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return listing_elements


def get_classroom_label(classroom):
    return '%s - %s' % (classroom.standard.number, classroom.division)