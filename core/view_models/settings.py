from core.view_models.base import AuthenticatedBody
from core.utils.view_model import get_classroom_label, get_user_label


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
        classroom = user.classes_enrolled_set.all()[0]  # user should be enrolled in 1 class only
        self.classroom = get_classroom_label(classroom)
        self.school = user.userinfo.school.name
        self.class_teacher = get_user_label(classroom.classTeacher)
        self.parents = [get_user_label(home.parent) for home in user.homes_enrolled_set.all()]


class ParentSettingsBody(SettingsBody):
    def __init__(self, user):
        raise


class AdminSettingsBody(SettingsBody):
    def __init__(self, user):
        raise


class TeacherSettingsBody(SettingsBody):
    def __init__(self, user):
        raise






