from core.models import ClassRoom
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils
from core.routing.urlnames import UrlNames
from core.utils.labels import get_classroom_label, get_subjectroom_label, get_user_label

# Note the templates only know about this Sidebar class and not its derived classes
from core.view_models.utils import Link


class UserInfo(object):
    """
    Container for storing user info
    """

    def __init__(self, user):
        self.user_school = user.userinfo.school.name
        self.name = get_user_label(user)
        self.user_id = user.pk


class StudentInfo(UserInfo):
    """
    Special container for student because student's userinfo also includes classroom label
    """

    def __init__(self, user):
        super(StudentInfo, self).__init__(user)
        self.classroom = get_classroom_label(user.classes_enrolled_set.get())

class Sidebar(object):
    """
    Common sidebar construct for all users
    """

    def __init__(self, user):
        self.userinfo = self.get_userinfo(user)
        self.type = user.userinfo.group
        self.TYPES = HWCentralGroup.refs

    def get_userinfo(self, user):
        return UserInfo(user)


class Ticker(object):
    """
    Container class to hold a generic ticker
    """

    def __init__(self, value, student_username):
        self.label = "Assignments To Do"
        self.link = Link(value, UrlNames.HOME.name, None, "active_assignment_table_%s" % student_username)


class SidebarListingElement(object):
    """
    Container to hold info for each element in a sidebar listing so a link can be built
    """

    def __init__(self, label, id):
        self.label = label
        self.id = id

class SidebarListing(object):
    """
    Just a container class to hold listing information
    """

    def __init__(self, title, urlname, elements):
        self.title = title
        self.urlname = urlname
        self.elements = elements


class StudentSidebar(Sidebar):
    # building ticker and listings

    def get_userinfo(self, user):
        # we will use student's custom userinfo which has classroom as well
        return StudentInfo(user)

    def __init__(self, user):
        super(StudentSidebar, self).__init__(user)

        utils = StudentUtils(user)

        # build the Ticker
        self.ticker = Ticker(utils.get_num_unfinished_assignments(), user.username)

        # build the Listings
        self.listings = []
        if user.subjects_enrolled_set.count() > 0:
            self.listings.append(SidebarListing(
                'Subjects',
                UrlNames.SUBJECT_ID.name,
                [SidebarListingElement(subjectroom.subject.name, subjectroom.pk) for subjectroom in
                 user.subjects_enrolled_set.all()]
            ))

class TeacherSidebar(Sidebar):
    def __init__(self, user):
        super(TeacherSidebar, self).__init__(user)

        # build the Listings
        self.listings = []
        if user.classes_managed_set.count() > 0:
            self.listings.append(SidebarListing(
                'ClassRooms',
                UrlNames.CLASSROOM_ID.name,
                [SidebarListingElement(get_classroom_label(classroom), classroom.pk) for classroom in
                 user.classes_managed_set.all()]
            ))
        if user.subjects_managed_set.count() > 0:
            self.listings.append(SidebarListing(
                'Subjects',
                UrlNames.SUBJECT_ID.name,
                [SidebarListingElement(get_subjectroom_label(subjectroom), subjectroom.pk) for subjectroom in
                 user.subjects_managed_set.all()]
            ))

class ParentSidebar(Sidebar):
    def __init__(self, user):
        super(ParentSidebar,self).__init__(user)
        self.child_sidebars = []
        for child in user.home.children.all():
            self.child_sidebars.append(StudentSidebar(child))

class AdminSidebar(Sidebar):
    def __init__(self, user):
        super(AdminSidebar, self).__init__(user)

        # build the Listings.
        self.listings = []
        if ClassRoom.objects.filter(school=user.userinfo.school).count() > 0:
            # TODO: later customize this to show grouping by standard which then breaks down by division
            classrooms = ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number',
                                                                                        'division')
            self.listings.append(SidebarListing(
                'Classrooms',
                UrlNames.CLASSROOM_ID.name,
                [SidebarListingElement(get_classroom_label(classroom), classroom.pk) for classroom in classrooms]
            ))
