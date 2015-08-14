from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBody
from core.utils.labels import get_classroom_label, get_user_label, get_subjectroom_label
from core.view_models.utils import Link, StudentInfo


class SettingsCommon(object):
    def __init__(self, user):
        self.user_label = get_user_label(user)
        self.username = user.username
        self.email = user.email
        self.school = user.userinfo.school.name

class SettingsBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the settings views
    """

    def __init__(self, user):
        self.settings_common = SettingsCommon(user)


class StudentSettingsBody(SettingsBody):
    """
    Construct the viewmodel for the student settings page body here. Information needed:
    1. Student classroom name
    2. Student school name
    3. Student class teacher name
    4. Student parent names as list
    """

    def __init__(self, user):
        super(StudentSettingsBody, self).__init__(user)
        classroom = user.classes_enrolled_set.get()  # user should be enrolled in 1 class only
        self.classroom = get_classroom_label(classroom)
        self.class_teacher = get_user_label(classroom.classTeacher)
        self.parents = [get_user_label(home.parent) for home in user.homes_enrolled_set.all()]


class ParentSettingsBody(SettingsBody):
    def __init__(self, user):
        super(ParentSettingsBody, self).__init__(user)
        self.child_list = []
        for child in user.home.children.all():
            self.child_list.append(StudentInfo(child))


class AdminSettingsBody(SettingsBody):
    def __init__(self, user):
        super(AdminSettingsBody, self).__init__(user)


class TeacherSettingsBody(SettingsBody):
    def __init__(self, user):
        super(TeacherSettingsBody, self).__init__(user)
        self.subject_listings = []
        for subject in user.subjects_managed_set.all():
            self.subject_listings.append(Link(get_subjectroom_label(subject), subject.pk, UrlNames.SUBJECT_ID.name))
