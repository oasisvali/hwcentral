from core.models import ClassRoom
from core.view_models.base import AuthenticatedBody
from core.utils.labels import get_classroom_label, get_user_label, get_subjectroom_label


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
    The viewmodel for the student settings page body
    """

    def __init__(self, user):
        super(StudentSettingsBody, self).__init__(user)
        classroom = user.classes_enrolled_set.get()  # user should be enrolled in 1 class only
        self.classroom = get_classroom_label(classroom)
        self.class_teacher = get_user_label(classroom.classTeacher)
        self.parents = [get_user_label(home.parent) for home in user.homes_enrolled_set.all()]


class ChildInfo(object):
    def __init__(self, child):
        self.name = get_user_label(child)
        classroom = child.classes_enrolled_set.get()
        self.classroom = get_classroom_label(classroom)
        self.classteacher = get_user_label(classroom.classTeacher)

class ParentSettingsBody(SettingsBody):
    def __init__(self, user):
        super(ParentSettingsBody, self).__init__(user)
        self.children = []
        for child in user.home.children.all():
            self.children.append(ChildInfo(child))

class AdminSettingsBody(SettingsBody):
    def __init__(self, user):
        super(AdminSettingsBody, self).__init__(user)
        self.classrooms = []
        for classroom in ClassRoom.objects.filter(school=user.userinfo.school):
            self.classrooms.append(get_classroom_label(classroom))

class TeacherSettingsBody(SettingsBody):
    def __init__(self, user):
        super(TeacherSettingsBody, self).__init__(user)
        self.subjectrooms = []
        for subjectroom in user.subjects_managed_set.all():
            self.subjectrooms.append(get_subjectroom_label(subjectroom))
        self.classrooms = []
        for classroom in user.classes_managed_set.all():
            self.classrooms.append(get_classroom_label(classroom))
