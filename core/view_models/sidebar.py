from core.models import ClassRoom
from core.utils.student import get_num_unfinished_assignments
from core.routing.urlnames import UrlNames
from core.utils.view_model import get_classroom_label, get_subjectroom_label, get_user_label

# Note the templates only know about this Sidebar class and not its derived classes
from core.view_models.link import Link

class Sidebar(object):
    """
    Common sidebar construct for all users
    """
    def __init__(self, user):
        self.user_school = user.userinfo.school.name
        self.name = get_user_label(user)


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
            subject_listing_elements.append(Link(get_subjectroom_label(subject), subject.pk))

        return subject_listing_elements


class StudentSidebar(Sidebar):

    #building ticker and listings

    def __init__(self, user):
        super(StudentSidebar, self).__init__(user)

        self.classroom = get_classroom_label(user.classes_enrolled_set.get())

        # build the Ticker
        self.ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENTS.name, get_num_unfinished_assignments(user))

        # build the Listings
        self.listings = []
        if user.subjects_enrolled_set.count() > 0:
            self.listings.append(SidebarListing('Subjects', UrlNames.SUBJECT_ID.name, self.get_subjects(user)))

    def get_subjects(self, user):
        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ParentSidebar(Sidebar):
    def __init__(self, user):

        #check for multiple children enrolled
        self.child_list= []
        if user.home.students.count() > 0:

            for child in user.home.students.all():
                self.child_list.append(StudentSidebar(child))

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