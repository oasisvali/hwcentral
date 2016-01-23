from django.db.models import Q
from django.forms.widgets import Select

from core.models import SubjectRoom
from core.utils.json import JSONModel
from core.utils.labels import get_user_label, get_subjectroom_label, get_fraction_label, AVERAGE_NA
from core.utils.references import HWCentralGroup
from core.view_models.base import AuthenticatedBody
from edge.models import StudentProficiency, SubjectRoomProficiency

UNSELECTED_OPTION = (0, "---------")


class EdgeBody(AuthenticatedBody):
    pass


class StudentIndexBody(EdgeBody):
    def __init__(self, student):
        subjectrooms = [(subjectroom.pk, subjectroom.subject.name) for subjectroom in
                        student.subjects_enrolled_set.all()]
        subjectrooms.insert(0, UNSELECTED_OPTION)

        self.subject_select = Select({'class': 'chosen-no-search', 'id': 'subject-select'}, subjectrooms).render(
            'subject', 0)


class ParentIndexBody(EdgeBody):
    def __init__(self, parent):
        child_options = [UNSELECTED_OPTION]
        self.subject_selects = []
        for child in parent.home.children.all():
            child_options.append((child.pk, get_user_label(child)))
            subject_options = [(subjectroom.pk, subjectroom.subject.name) for subjectroom in
                               child.subjects_enrolled_set.all()]
            subject_select = Select({'class': 'chosen-no-search', 'id': 'subject-select-' + str(child.pk)},
                                    subject_options)
            self.subject_selects.append(subject_select.render('subject_child' + str(child.pk), 0))

        self.child_select = Select({'class': 'chosen-no-search', 'id': 'child-select'},
                                   child_options).render('child', 0)


class TeacherAdminIndexBase(EdgeBody):
    """
    Abstract class to reduce duplication
    """

    def get_subjectrooms(self):
        raise NotImplementedError("Subclass of TeacherAdminIndexBody must implement get_subjectrooms")

    def __init__(self):
        subjectrooms = self.get_subjectrooms()

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


class TeacherIndexBody(TeacherAdminIndexBase):
    def __init__(self, teacher):
        self.teacher = teacher
        super(TeacherIndexBody, self).__init__()

    def get_subjectrooms(self):
        return SubjectRoom.objects.filter(Q(teacher=self.teacher) | Q(classRoom__classTeacher=self.teacher)).order_by(
                'pk')



class AdminIndexBody(EdgeBody):
    def get_subjectrooms(self):
        return SubjectRoom.objects.filter(classRoom__school=self.admin.userinfo.school)

    def __init__(self, admin):
        self.admin = admin
        super(AdminIndexBody, self).__init__()


class PositiveNegativeElem(JSONModel):
    def __init__(self, proficiency):
        self.title = proficiency.questiontag.name
        self.score = get_fraction_label(proficiency.score)


class PositiveNegativeBase(JSONModel):
    def __init__(self, positive, negative, application, conceptual, critical):
        self.positive = positive
        self.negative = negative
        self.application = get_fraction_label(application.score) if application is not None else AVERAGE_NA
        self.conceptual = get_fraction_label(conceptual.score) if conceptual is not None else AVERAGE_NA
        self.critical = get_fraction_label(critical.score) if critical is not None else AVERAGE_NA

class StudentPositiveNegative(PositiveNegativeBase):
    def __init__(self, student, subjectroom):
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        positive = [PositiveNegativeElem(proficiency) for proficiency in
                    StudentProficiency.get_positives(subjectroom, Q(student=student))]
        negative = [PositiveNegativeElem(proficiency) for proficiency in
                    StudentProficiency.get_negatives(subjectroom, Q(student=student))]

        application, conceptual, critical = StudentProficiency.get_special_tags(subjectroom, Q(student=student))

        super(StudentPositiveNegative, self).__init__(positive, negative, application, conceptual, critical)


class SubjectRoomPositiveNegative(PositiveNegativeBase):
    def __init__(self, subjectroom):
        positive = [PositiveNegativeElem(proficiency) for proficiency in
                    SubjectRoomProficiency.get_positives(subjectroom)]
        negative = [PositiveNegativeElem(proficiency) for proficiency in
                    SubjectRoomProficiency.get_negatives(subjectroom)]

        application, conceptual, critical = SubjectRoomProficiency.get_special_tags(subjectroom)

        super(SubjectRoomPositiveNegative, self).__init__(positive, negative, application, conceptual, critical)
