from django.db.models import Q
from django.forms.widgets import Select

from core.models import SubjectRoom
from core.utils.json import JSONModel
from core.utils.labels import get_user_label, get_subjectroom_label, get_fraction_label
from core.utils.references import HWCentralGroup
from core.view_models.base import AuthenticatedBody
from edge.models import Proficiency, SubjectRoomProficiency

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


class PositiveNegativeElem(JSONModel):
    def __init__(self, proficiency):
        self.title = proficiency.questiontag.name
        self.basic = get_fraction_label(0.7 * proficiency.rate)
        self.relative = get_fraction_label(0.3 * proficiency.percentile)


class PositiveNegativeBase(JSONModel):
    def __init__(self, positive, negative):
        self.positive = positive
        self.negative = negative


class StudentPositiveNegative(PositiveNegativeBase):
    def __init__(self, student):
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        positive_proficiency = Proficiency.objects.filter(student=student, score__gte=0.8).order_by('-score')
        negative_proficiency = Proficiency.objects.filter(student=student, score__lte=0.4).order_by('-score')

        positive = [PositiveNegativeElem(proficiency) for proficiency in positive_proficiency]
        negative = [PositiveNegativeElem(proficiency) for proficiency in negative_proficiency]

        super(StudentPositiveNegative, self).__init__(positive, negative)


class SubjectRoomPositiveNegative(PositiveNegativeBase):
    def __init__(self, subjectroom):
        positive_proficiency = SubjectRoomProficiency.objects.filter(subjectRoom=subjectroom, score__gte=0.8).order_by(
            '-score')
        negative_proficiency = SubjectRoomProficiency.objects.filter(subjectRoom=subjectroom, score__lte=0.4).order_by(
            '-score')

        positive = [PositiveNegativeElem(proficiency) for proficiency in positive_proficiency]
        negative = [PositiveNegativeElem(proficiency) for proficiency in negative_proficiency]

        super(SubjectRoomPositiveNegative, self).__init__(positive, negative)
