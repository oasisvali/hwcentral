from core.models import ClassRoom, Assignment, Submission
from core.modules.constants import HWCentralGroup
from core.routing.urlnames import UrlNames
from core.view_models.util import Link
from hwcentral.exceptions import InvalidStateException

# prob belongs in a student_utils class
def num_unfinished_assignments(user):
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # build a list of all assignments - TODO: this might be possible to do in a single query
    assignments = []
    for subject in user.subjects_enrolled_set.all():
        assignments.extend(list(Assignment.objects.filter(subjectRoom=subject)))

    # check if 100% submissions have been posted for each assignment
    unfinished_assignments = 0
    for assignment in assignments:
        if Submission.objects.filter(assignment=assignment).filter(completion=1).count() == 0:
            unfinished_assignments += 1
    return unfinished_assignments


class Sidebar(object):
    def __init__(self, user):
        self.user_group = user.userinfo.group.pk
        self.user_groupname = user.userinfo.group.name
        self.user_fullname = '%s %s' % (user.first_name, user.last_name)
        self.user_school = user.userinfo.school.name
        self.ticker = None

        self.school_urlname = UrlNames.SCHOOL.name
        self.fullname_urlname = UrlNames.HOME.name

        self.listings = []

        if self.user_group == HWCentralGroup.TEACHER:
            if user.classes_managed_set.count() > 0:
                self.listings.append(TeacherClassroomsSidebarListing(user.classes_managed_set.all()))
            if user.subjects_managed_set.count() > 0:
                self.listings.append(TeacherSubjectsSidebarListing(user.subjects_managed_set.all()))
        elif self.user_group == HWCentralGroup.PARENT:
            if user.home.students.count() > 0:
                self.listings.append(ParentSidebarListing(user, self.user_group))
        elif self.user_group == HWCentralGroup.STUDENT:
            if user.subjects_enrolled_set.count() > 0:
                self.listings.append(StudentSidebarListing(user, self.user_group))
            self.ticker = Ticker("Unfinished Assignments", UrlNames.ASSIGNMENT.name, num_unfinished_assignments(user))
        elif self.user_group == HWCentralGroup.ADMIN:
            if ClassRoom.objects.filter(school=user.userinfo.school).count() > 0:
                self.listings.append(AdminSidebarListing(user, self.user_group))
        else:
            raise InvalidStateException('Invalid HWCentralGroup: %s' % user.userinfo.group.name)


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
    def __init__(self, classrooms):
        super(TeacherClassroomsSidebarListing, self).__init__('Classrooms', UrlNames.CLASSROOM.name,
                                                              self.get_classroom_listing_elements(classrooms))

    def get_classroom_listing_elements(self, classrooms):
        classroom_listing_elements = []
        for classroom in classrooms:
            classroom_listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return classroom_listing_elements


class TeacherSubjectsSidebarListing(SidebarListing):
    def __init__(self, subjects):
        super(TeacherSubjectsSidebarListing, self).__init__('Subjects', UrlNames.SUBJECT.name,
                                                            self.get_subject_listing_elements(subjects))

    def get_subject_listing_elements(self, subjects):
        subject_listing_elements = []
        for subject in subjects:
            subject_listing_elements.append(Link('%s : %s - %s' % (subject.subject.name, subject.classRoom.standard,
                                                                   subject.classRoom.division), subject.pk))

        return subject_listing_elements


class StudentSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(StudentSidebarListing, self).__init__('Subjects', UrlNames.SUBJECT.name,
                                                    self.get_subjects(user, user_group))

    def get_subjects(self, user, user_group):
        assert user_group == HWCentralGroup.STUDENT

        listing_elements = []
        for subject in user.subjects_enrolled_set.all():
            listing_elements.append(Link(subject.subject.name, subject.pk))

        return listing_elements


class ParentSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(ParentSidebarListing, self).__init__('Students', UrlNames.STUDENT.name,
                                                   self.get_students(user, user_group))

    def get_students(self, user, user_group):
        assert user_group == HWCentralGroup.PARENT

        listing_elements = []
        for student in user.home.students.all():
            listing_elements.append(Link('%s %s' % (student.first_name, student.last_name), student.username))

        return listing_elements


class AdminSidebarListing(SidebarListing):
    def __init__(self, user, user_group):
        super(AdminSidebarListing, self).__init__('Classrooms', UrlNames.CLASSROOM.name,
                                                  self.get_classrooms(user, user_group))

    def get_classrooms(self, user, user_group):
        assert user_group == HWCentralGroup.ADMIN

        listing_elements = []
        for classroom in ClassRoom.objects.filter(school=user.userinfo.school).order_by('-standard__number',
                                                                                        'division'):
            # TODO: later customize this to show grouping by standard which then breaks down by division
            listing_elements.append(Link(get_classroom_label(classroom), classroom.pk))

        return listing_elements


def get_classroom_label(classroom):
    return '%s - %s' % (classroom.standard.number, classroom.division)