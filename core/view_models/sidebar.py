from django.core.urlresolvers import reverse

from cabinet.cabinet_api import get_school_stamp_url_secure
from core.models import ClassRoom
from core.routing.urlnames import UrlNames
from core.utils.labels import get_classroom_label, get_subjectroom_label, get_focusroom_label, get_fraction_label
from core.utils.open_student import OpenStudentUtils
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils
# Note the templates only know about this Sidebar class and not its derived classes
from core.view_models.userinfo import BaseUserInfo
from core.view_models.utils import Link
from hwcentral.exceptions import InvalidStateError


class ChildInfo(BaseUserInfo):
    """
    Special container for child because child's info to be shown in parent sidebar also includes classroom label
    """

    def __init__(self, user):
        super(ChildInfo, self).__init__(user)
        self.classroom = get_classroom_label(user.classes_enrolled_set.get())


class SidebarTypes(object):
    def __init__(self, user):
        self.type = user.userinfo.group
        self.TYPES = HWCentralGroup.refs


class Sidebar(SidebarTypes):
    """
    Common sidebar construct for all users (except open)
    """

    def __init__(self, user):
        super(Sidebar, self).__init__(user)
        self.school_stamp_url = get_school_stamp_url_secure(user)
        self.school_stamp_title = "Return to home page"
        self.school_stamp_href = reverse(UrlNames.INDEX.name)


class Ticker(object):
    """
    Container class to hold a generic ticker
    """

    # TODO: no need to tag with username since no ticker linking for parent anymore
    def __init__(self, value, student_username, label):
        self.label = label
        self.link = Link(value, UrlNames.HOME.name, None, "ticker_anchor_%s" % student_username)


class ParentChildTicker(object):
    def __init__(self, value, label="Assignments"):
        self.label = label
        self.value = value

class SidebarListing(object):
    """
    Just a container class to hold listing information
    """

    def __init__(self, title, elements):
        self.title = title
        self.elements = elements


class ProficiencyClass(object):
    KING = 'king'
    KNIGHT = 'knight'
    PAWN = 'pawn'

    RANKING = {
        KING: 1,
        KNIGHT: 2,
        PAWN: 3
    }

    def __init__(self, value):
        if value > 0.8:
            self.name = ProficiencyClass.KING
        elif value > 0.5:
            self.name = ProficiencyClass.KNIGHT
        elif value > 0:
            self.name = ProficiencyClass.PAWN
        else:
            self.name = None

    @classmethod
    def create_message(cls, proficiency_class, standard, subject):
        if proficiency_class == ProficiencyClass.KING:
            return "Congratulations! You have successfully mastered 80&37; of Grade %s %s content" % (standard, subject)

        elif proficiency_class == ProficiencyClass.KNIGHT:
            return "Congratulations! You have been Knighted for correctly answering half of the total content for Grade %s %s" % (
            standard, subject)

        elif proficiency_class == ProficiencyClass.PAWN:
            return "Congratulations! You have successfully started your journey towards mastering Grade %s %s" % (
            standard, subject)

        else:
            raise InvalidStateError(proficiency_class)

    def __str__(self):
        return self.name

    def __nonzero__(self):
        return self.name is not None

    def __eq__(self, other):
        """
        Enables equality comparison as long as ProfciencyClass object is on LHS
        """
        if isinstance(other, ProficiencyClass):
            return self.name == other.name

        return self.name == other

    def __ge__(self, other):
        assert other is not None
        if self.name is None:
            return False
        return ProficiencyClass.RANKING[self.name] <= ProficiencyClass.RANKING[other]


class ProgressListingElement(object):
    def __init__(self, link, completion, proficiency):
        self.link = link
        self.completion = get_fraction_label(completion)
        self.proficiency = get_fraction_label(proficiency)
        self.proficiency_class = ProficiencyClass(proficiency)

class StudentSidebarBase(Sidebar):
    def __init__(self, user):
        super(StudentSidebarBase, self).__init__(user)

        # build the Listings
        self.listings = []
        if user.subjects_enrolled_set.count() > 0:
            self.listings.append(SidebarListing(
                'Subjects',
                [Link(subjectroom.subject.name, UrlNames.SUBJECT_ID.name, subjectroom.pk) for subjectroom in
                 user.subjects_enrolled_set.all()]
            ))

            if user.userinfo.school.schoolprofile.focus:
                self.listings.append(SidebarListing(
                    'Focus Groups',
                    [Link(get_focusroom_label(subjectroom.subject.name), UrlNames.FOCUS_ID.name,
                          subjectroom.focusroom.pk)
                     for
                     subjectroom in
                     user.subjects_enrolled_set.all()]
                ))


class StudentSidebar(StudentSidebarBase):
    def __init__(self, user):
        super(StudentSidebar, self).__init__(user)

        utils = StudentUtils(user)

        # build the Ticker
        self.ticker = Ticker(utils.get_num_unfinished_assignments(), user.username, "Assignments")


class OpenStudentSidebar(Sidebar):
    def __init__(self, user):
        super(OpenStudentSidebar, self).__init__(user)
        self.school_stamp_title = "OpenShiksha is an initiative by Social Seva"
        self.school_stamp_href = "http://socialseva.org/"
        self.school_stamp_class = 'open-school'
        self.school_stamp_target = '_blank'

        utils = OpenStudentUtils(user)

        # build the Ticker
        self.ticker = Ticker(utils.get_num_unfinished_assignments(), user.username, "Active Assignments")

        # build the Listings
        listing_elements = []

        for subjectroom in user.subjects_enrolled_set.all():
            listing_elements.append(
                ProgressListingElement(
                    Link(subjectroom.subject.name, UrlNames.SUBJECT_ID.name, subjectroom.pk),
                    utils.get_completion(subjectroom),
                    utils.get_proficiency(subjectroom)
                )
            )

        self.listings = [SidebarListing('Student Profile', listing_elements)]


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
                [Link(get_classroom_label(classroom), UrlNames.CLASSROOM_ID.name, classroom.pk) for classroom in
                 user.classes_managed_set.all()]
            ))
        if user.subjects_managed_set.exists():
            self.listings.append(SidebarListing(
                'SubjectRooms',
                [Link(get_subjectroom_label(subjectroom), UrlNames.SUBJECT_ID.name, subjectroom.pk) for subjectroom in
                 user.subjects_managed_set.all()]
            ))

            if user.userinfo.school.schoolprofile.focus:
                self.listings.append(SidebarListing(
                    'FocusRooms',
                    [Link(get_focusroom_label(get_subjectroom_label(subjectroom)),
                          UrlNames.FOCUS_ID.name, subjectroom.focusroom.pk) for subjectroom in
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
                [Link(get_classroom_label(classroom), UrlNames.CLASSROOM_ID.name, classroom.pk) for classroom in
                 classrooms]
            ))
