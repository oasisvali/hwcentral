from django.db.models import Q
from django.forms.widgets import Select

from cabinet.cabinet_api import get_question_with_img_urls
from core.models import SubjectRoom
from core.utils.json import JSONModel
from core.utils.labels import get_user_label, get_subjectroom_label, get_percentage_label
from core.utils.references import HWCentralGroup
from core.view_models.base import AuthenticatedBody
from edge.models import StudentProficiency, SubjectRoomProficiency, SubjectRoomQuestionMistake

UNSELECTED_OPTION = (0, "---------")


class EdgeBody(AuthenticatedBody):
    pass


class StudentIndexBody(EdgeBody):
    def __init__(self, student):
        subjectrooms = [(subjectroom.pk, subjectroom.subject.name) for subjectroom in
                        student.subjects_enrolled_set.all()]
        subjectrooms.insert(0, UNSELECTED_OPTION)

        self.subject_select = Select({'class': 'chosen-no-search chosen-smaller', 'id': 'subject-select'},
                                     subjectrooms).render(
            'subject', 0)


class ParentIndexBody(EdgeBody):
    def __init__(self, parent):
        child_options = [UNSELECTED_OPTION]
        self.subject_selects = []
        for child in parent.home.children.all():
            child_options.append((child.pk, get_user_label(child)))
            subject_options = [(subjectroom.pk, subjectroom.subject.name) for subjectroom in
                               child.subjects_enrolled_set.all()]
            subject_select = Select({'id': 'subject-select-' + str(child.pk)},
                                    subject_options)
            self.subject_selects.append(subject_select.render('subject_child' + str(child.pk), 0))

        self.child_select = Select({'class': 'chosen-no-search chosen-smaller', 'id': 'child-select'},
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


class AdminIndexBody(TeacherAdminIndexBase):
    def get_subjectrooms(self):
        return SubjectRoom.objects.filter(classRoom__school=self.admin.userinfo.school)

    def __init__(self, admin):
        self.admin = admin
        super(AdminIndexBody, self).__init__()


class ProficiencyVM(JSONModel):
    @classmethod
    def from_proficiency(cls, proficiency):
        return cls(proficiency.questiontag, get_percentage_label(proficiency.score))

    @classmethod
    def build_shell(cls, questiontag):
        return cls(questiontag, '---')

    def __init__(self, questiontag, score):
        self.title = questiontag.name.title()
        self.score = score


class EdgeDataBase(JSONModel):
    def __init__(self, positive, negative, application, conceptual, critical, tablerows):
        self.positive = positive
        self.negative = negative
        self.application = application
        self.conceptual = conceptual
        self.critical = critical
        self.tablerows = tablerows


class StudentEdgeData(EdgeDataBase):
    def __init__(self, student, subjectroom):
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        positive = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                    StudentProficiency.get_positives(subjectroom, Q(student=student))]
        negative = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                    StudentProficiency.get_negatives(subjectroom, Q(student=student))]

        application, conceptual, critical = StudentProficiency.get_special_tags(subjectroom, Q(student=student))

        tablerows = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                     StudentProficiency.objects.filter(student=student, subjectRoom=subjectroom).order_by('score')]

        super(StudentEdgeData, self).__init__(positive, negative, application, conceptual, critical, tablerows)


class QuestionPreview(JSONModel):
    def __init__(self, user, question_db):
        undealt_question_dm = get_question_with_img_urls(user, question_db)
        self.data_model = undealt_question_dm.deal()


class SubjectRoomEdgeData(EdgeDataBase):
    def __init__(self, user, subjectroom):
        positive = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                    SubjectRoomProficiency.get_positives(subjectroom)]
        negative = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                    SubjectRoomProficiency.get_negatives(subjectroom)]

        application, conceptual, critical = SubjectRoomProficiency.get_special_tags(subjectroom)

        tablerows = [ProficiencyVM.from_proficiency(proficiency) for proficiency in
                     SubjectRoomProficiency.objects.filter(subjectRoom=subjectroom).order_by('score')]

        super(SubjectRoomEdgeData, self).__init__(positive, negative, application, conceptual, critical, tablerows)

        self.questions = [QuestionPreview(user, subjectroom_question_mistake.question) for subjectroom_question_mistake
                          in SubjectRoomQuestionMistake.objects.filter(subjectRoom=subjectroom).order_by('-regression')[
                             :3]]
