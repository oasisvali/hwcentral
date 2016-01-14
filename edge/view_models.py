from django.db.models import Q
from django.forms.widgets import Select

from core.models import SubjectRoom
from core.utils.labels import get_user_label, get_subjectroom_label
from core.view_models.base import AuthenticatedBody

UNSELECTED_OPTION = (0, "---------")


class EdgeBody(AuthenticatedBody):
    pass


class StudentIndexBody(EdgeBody):
    pass


class ParentIndexBody(EdgeBody):
    def __init__(self, parent):
        children = [(child.pk, get_user_label(child)) for child in parent.home.children.all()]
        children.insert(0, UNSELECTED_OPTION)

        self.child_select = Select({'class': 'chosen-no-search', 'id': 'child-select'}, children).render('child', 0)


class TeacherIndexBody(EdgeBody):
    def __init__(self, teacher):
        subjectrooms = SubjectRoom.objects.filter(Q(teacher=teacher) | Q(classRoom__classTeacher=teacher)).order_by(
            'pk')

        subjectroom_options = [UNSELECTED_OPTION]
        self.student_selects = []
        for subjectroom in subjectrooms:
            subjectroom_options.append((subjectroom.pk, get_subjectroom_label(subjectroom)))
            student_options = [(student.pk, get_user_label(student)) for student in subjectroom.students.all()]
            student_options.insert(0, (0, "Full Class"))
            student_select = Select({'id': 'student-select-' + str(subjectroom.pk)}, student_options)
            self.student_selects.append(student_select.render('student_subjectroom' + str(subjectroom.pk), 0))

        self.subjectroom_select = Select({'class': 'chosen-no-search chosen-smaller', 'id': 'subjectroom-select'},
                                         subjectroom_options).render('subjectroom', 0)


class AdminIndexBody(EdgeBody):
    def __init__(self, admin):
        subjectrooms = SubjectRoom.objects.filter(classRoom__school=admin.userinfo.school)

        subjectroom_options = [UNSELECTED_OPTION]
        self.student_selects = []
        for subjectroom in subjectrooms:
            subjectroom_options.append((subjectroom.pk, get_subjectroom_label(subjectroom)))
            student_options = [(student.pk, get_user_label(student)) for student in subjectroom.students.all()]
            student_options.insert(0, (0, "Full Class"))
            student_select = Select({'id': 'student-select-' + str(subjectroom.pk)}, student_options)
            self.student_selects.append(student_select.render('student_subjectroom' + str(subjectroom.pk), 0))

        self.subjectroom_select = Select({'class': 'chosen-no-search chosen-smaller', 'id': 'subjectroom-select'},
                                         subjectroom_options).render('subjectroom', 0)
