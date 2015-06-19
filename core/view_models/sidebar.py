from core.models import ClassRoom
from core.utils.student import get_num_unfinished_assignments
from core.routing.urlnames import UrlNames
from core.utils.view_model import get_classroom_label

# Note the templates only know about this Sidebar class and not its derived classes
from core.view_models.link import Link

class Sidebar(object):
    """
    Common sidebar construct for all users
    """
    def __init__(self, user):
        self.user_school = user.userinfo.school.name


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


class TeacherSidebar(Sidebar):
    def __init__(self, user):
        # build the Listings
        self.classroom_listings = []
        if user.classes_managed_set.count() > 0:
            self.classroom_listings.append(SidebarListing('Classrooms', UrlNames.CLASSROOM.name,
                                           self.get_classroom_listing_elements(user)))
        self.subject_listings = []
        if user.subjects_managed_set.count() > 0:
            self.subject_listings.append(SidebarListing('Subjects', UrlNames.SUBJECT_ID.name,
                                           self.get_subject_listing_elements(user)))

        super(TeacherSidebar, self).__init__(user)
        

    def get_classroom_listing_elements(self, user):
        classroom_listing_elements = []
        for classroom in user.classes_managed_set.all():
            classroom_listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return classroom_listing_elements

    def get_subject_listing_elements(self, user):
        subject_listing_elements = []
        for subject in user.subjects_managed_set.all():
            subject_listing_elements.append(Link('%s : %s - %s' % (subject.subject.name, subject.classRoom.standard,
                                                                   subject.classRoom.division), subject.pk))

        return subject_listing_elements


class StudentSidebar(Sidebar):

    #building ticker and listings

    def __init__(self, user):
        # build the Ticker
        self.ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENTS.name, get_num_unfinished_assignments(user))

        # build the Listings
        self.listings = []
        if user.subjects_enrolled_set.count() > 0:
            self.listings.append(SidebarListing('Subjects', UrlNames.SUBJECT_ID.name, self.get_subjects(user)))

        super(StudentSidebar, self).__init__(user)

    def get_subjects(self, user):
        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ChildInfo(object):
    def __init__(self, child):
        child_class = child.classes_enrolled_set.all()[:1][0]
        self.child = child
        self.standard = child_class.standard.number
        self.division = child_class.division

class ParentChild (object):
    """
    Parent sidebar construct
    """
    def __init__(self,child):
        self.child_info = ChildInfo(child)
        #student sidebar elements called in the construct
        self.child_sidebar_info =StudentSidebar(child)

class ParentSidebar(Sidebar):
    def __init__(self, user):

        #check for multiple children enrolled
        self.child_list= []
        if user.home.students.count() > 0:

            for child in user.home.students.all():
                self.child_list.append(ParentChild(child))

        super(ParentSidebar,self).__init__(user)


class AdminSidebar(Sidebar):
    def __init__(self, user):

        # build the Listings.
        self.listings = []
        if ClassRoom.objects.filter(school=user.userinfo.school).count() > 0:
            self.listings.append(SidebarListing('Classrooms', UrlNames.CLASSROOM.name,
                                           self.get_classrooms(user)))

        super(AdminSidebar, self).__init__(user)

    def get_classrooms(self, user):
        listing_elements = []
        for classroom in ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number',
                                                                                        'division'):
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return listing_elements