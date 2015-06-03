from core.models import ClassRoom
from core.utils.student import get_num_unfinished_assignments ,get_list_active_subject_assignments
from core.routing.urlnames import UrlNames
from core.utils.view_model import Link, get_classroom_label

# Note the templates only know about this Sidebar class and not its derived classes
class Sidebar(object):
    def __init__(self, user, listings, ticker=None):
        self.user_school = user.userinfo.school.name

        self.ticker = ticker
        self.listings = listings

class Parent_trend_graph(object):
    """

    for the graph in the parent view to get info on the student's subject and avg and class teacher etc
    """
    def __init__(self, user, sub_listings , average,  sub_ticker=None):

        self.user_subjects = user.userinfo.school.name
        self.sub_ticker = sub_ticker
        self.listings = sub_listings
        self.average = average

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
        # build the Ticker
        ticker = None

        # build the Listings
        listings = []
        if user.classes_managed_set.count() > 0:
            listings.append(SidebarListing('Classrooms', UrlNames.CLASSROOM.name,
                                           self.get_classroom_listing_elements(user)))
        if user.subjects_managed_set.count() > 0:
            listings.append(SidebarListing('Subjects', UrlNames.SUBJECT_ID.name,
                                           self.get_subject_listing_elements(user)))

        super(Sidebar, self).__init__(user, listings, ticker)

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
    def __init__(self, user):
        # build the Ticker
        ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENTS.name, get_num_unfinished_assignments(user))

        # build the Listings
        listings = []
        if user.subjects_enrolled_set.count() > 0:
            listings.append(SidebarListing('Subjects', UrlNames.SUBJECT_ID.name, self.get_subjects(user)))

        super(StudentSidebar, self).__init__(user, listings, ticker)

    def get_subjects(self, user):
        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ParentSidebar(Sidebar):
    def __init__(self, user):
        # build the Ticker
        #sub_ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENTS.name, get_list_active_subject_assignments(user,subject = subject))
        ticker = None
        # build the Listings
        listings = []
        if user.home.students.count() > 0:
            listings.append(SidebarListing('Students', UrlNames.STUDENT.name,
                                           self.get_students(user)))

        super(Sidebar, self).__init__(user, listings, ticker)

        for student in listings:
            listing_subject =[]
            for subject in student.subjects_enrolled_set.all():
                listing_subject.append(Link(subject.subject.name, subject.pk))

            super(StudentSidebar,self).__init__(student,listing_subject,ticker)



        #super(Graph.self).__init__(user,sub_listings, average, sub_ticker)

    def get_students(self, user):
        listing_elements = []
        for student in user.home.students.all():
            listing_elements.append(Link('%s %s' % (student.first_name, student.last_name), student.username))
        return listing_elements

    def get_subjects(self, user):
        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements

class AdminSidebar(Sidebar):
    def __init__(self, user):
        # build the Ticker
        ticker = None

        # build the Listings
        listings = []
        if ClassRoom.objects.filter(school=user.userinfo.school).count() > 0:
            listings.append(SidebarListing('Classrooms', UrlNames.CLASSROOM.name,
                                           self.get_classrooms(user)))

        super(Sidebar, self).__init__(user, listings, ticker)

    def get_classrooms(self, user):
        listing_elements = []
        for classroom in ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number',
                                                                                        'division'):
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return listing_elements