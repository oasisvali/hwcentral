from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBody
from core.utils.labels import get_classroom_label, get_user_label, get_subjectroom_label
from core.view_models.utils import Link, StudentInfo


class SettingsBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the settings views
    """

    def __init__(self):
        pass


class StudentSettingsBody(SettingsBody):
    """
    Construct the viewmodel for the student settings page body here. Information needed:
    1. Student classroom name
    2. Student school name
    3. Student class teacher name
    4. Student parent names as list
    """

    def __init__(self, user):
        classroom = user.classes_enrolled_set.get()  # user should be enrolled in 1 class only
        self.classroom = get_classroom_label(classroom)
        self.school = user.userinfo.school.name
        self.class_teacher = get_user_label(classroom.classTeacher)
        self.parents = [get_user_label(home.parent) for home in user.homes_enrolled_set.all()]


class ParentSettingsBody(SettingsBody):
    def __init__(self, user):
        self.school = user.userinfo.school.name
        self.child_list = []
        for child in user.home.students.all():
            self.child_list.append(StudentInfo(child))


class AdminSettingsBody(SettingsBody):
    def __init__(self, user):
        self.school = user.userinfo.school.name



class TeacherSettingsBody(SettingsBody):
    def __init__(self, user):
        self.school = user.userinfo.school.name
        self.subject_listings = []
        for subject in user.subjects_managed_set.all():
            self.subject_listings.append(Link(get_subjectroom_label(subject), subject.pk, UrlNames.SUBJECT_ID.name))
