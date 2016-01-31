from cabinet.cabinet_api import get_school_stamp_url_secure
from core.models import ClassRoom
from core.routing.urlnames import UrlNames
from core.utils.labels import get_classroom_label, get_subjectroom_label, get_focusroom_label
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils
# Note the templates only know about this Sidebar class and not its derived classes
from core.view_models.userinfo import BaseUserInfo
from core.view_models.utils import Link


class ChildInfo(BaseUserInfo):
    """
    Special container for child because child's info to be shown in parent sidebar also includes classroom label
    """

    def __init__(self, user):
        super(ChildInfo, self).__init__(user)
        self.classroom = get_classroom_label(user.classes_enrolled_set.get())

class Sidebar(object):
    """
    Common sidebar construct for all users
    """

    def __init__(self, user):
        self.type = user.userinfo.group
        self.TYPES = HWCentralGroup.refs
        self.school_stamp_url = get_school_stamp_url_secure(user)


class TickerBase(object):
    label = "Assignments"


class Ticker(TickerBase):
    """
    Container class to hold a generic ticker
    """

    # TODO: no need to tag with username since no ticker linking for parent anymore
    def __init__(self, value, student_username):
        self.link = Link(value, UrlNames.HOME.name, None, "active_assignment_table_%s" % student_username)


class ParentChildTicker(TickerBase):
    def __init__(self, value):
        self.value = value


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


class StudentSidebarBase(Sidebar):
    def __init__(self, user):
        super(StudentSidebarBase, self).__init__(user)

        # build the Listings
        self.listings = []
        if user.subjects_enrolled_set.count() > 0:
            self.listings.append(SidebarListing(
                'Subjects',
                UrlNames.SUBJECT_ID.name,
                [SidebarListingElement(subjectroom.subject.name, subjectroom.pk) for subjectroom in
                 user.subjects_enrolled_set.all()]
            ))
            self.listings.append(SidebarListing(
                    'Focus Groups',
                    UrlNames.FOCUS_ID.name,
                    [SidebarListingElement(get_focusroom_label(subjectroom.subject.name), subjectroom.focusroom.pk) for
                     subjectroom in
                     user.subjects_enrolled_set.all()]
            ))


class StudentSidebar(StudentSidebarBase):
    def __init__(self, user):
        super(StudentSidebar, self).__init__(user)

        utils = StudentUtils(user)

        # build the Ticker
        self.ticker = Ticker(utils.get_num_unfinished_assignments(), user.username)


class ChildSidebar(StudentSidebarBase):
    def __init__(self, user):
        super(ChildSidebar, self).__init__(user)

        utils = StudentUtils(user)

        # build the Ticker
        self.ticker = ParentChildTicker(utils.get_num_unfinished_assignments())

class TeacherSidebar(Sidebar):
    def __init__(self, user):
        super(TeacherSidebar, self).__init__(user)

        # build the Listings
        self.listings = []
        if user.classes_managed_set.exists():
            self.listings.append(SidebarListing(
                'ClassRooms',
                UrlNames.CLASSROOM_ID.name,
                [SidebarListingElement(get_classroom_label(classroom), classroom.pk) for classroom in
                 user.classes_managed_set.all()]
            ))
        if user.subjects_managed_set.exists():
            self.listings.append(SidebarListing(
                'SubjectRooms',
                UrlNames.SUBJECT_ID.name,
                [SidebarListingElement(get_subjectroom_label(subjectroom), subjectroom.pk) for subjectroom in
                 user.subjects_managed_set.all()]
            ))
            self.listings.append(SidebarListing(
                    'FocusRooms',
                    UrlNames.FOCUS_ID.name,
                    [SidebarListingElement(get_focusroom_label(get_subjectroom_label(subjectroom)),
                                           subjectroom.focusroom.pk) for subjectroom in
                 user.subjects_managed_set.all()]
            ))

class ParentSidebar(Sidebar):
    def __init__(self, user):
        super(ParentSidebar,self).__init__(user)
        self.child_sidebars = []
        for child in user.home.children.all():
            self.child_sidebars.append((ChildInfo(child), ChildSidebar(child)))

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
                'ClassRooms',
                UrlNames.CLASSROOM_ID.name,
                [SidebarListingElement(get_classroom_label(classroom), classroom.pk) for classroom in classrooms]
            ))
