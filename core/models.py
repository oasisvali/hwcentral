from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from core.utils.labels import get_classroom_label, get_subjectroom_label, get_user_label
from core.utils.user_checks import is_hwcentral_team_admin
from hwcentral.exceptions import InvalidContentTypeError
from hwcentral.settings import MAX_CHARFIELD_LENGTH

CORE_APP_LABEL = 'core'
FRACTION_VALIDATOR = [
    MinValueValidator(0.0),
    MaxValueValidator(1.0)
]

# NOTE: DJANGO ADDS AUTO-INCREMENTING PRIMARY KEY TO MODELS AUTOMATICALLY WHEN NO PRIMARY KEY HAS BEEN DEFINEED
#	    THESE PRIMARY KEYS ARE ACCESSIBLE AS 'pk' ATTRIBUTE

MAX_TEXTFIELD_LENGTH = 1000


# BASIC MODELS - These are used as simple id-name key-value pairs

class Group(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH,
                            help_text='A string descriptor for the user group.')

    def __unicode__(self):
        return unicode(self.name)


class Board(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH,
                            help_text='A string descriptor for the board.')

    def __unicode__(self):
        return unicode(self.name)


# using a seperate model instead of simply a PositiveIntegerField to create control over supported standard values
class Standard(models.Model):
    number = models.PositiveIntegerField(unique=True, help_text='A positive integer representing the standard.')

    def __unicode__(self):
        return unicode(self.number)


class Subject(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH,
                            help_text='A string descriptor for the subject.')

    def __unicode__(self):
        return unicode(self.name)


class Chapter(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH,
                            help_text='A string descriptor for the chapter.')

    def __unicode__(self):
        return unicode(self.name)


class QuestionTag(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH,
                            help_text='A string descriptor for the question tag.')

    def __unicode__(self):
        return unicode(self.name)


# COMPLEX MODELS - These form the basis of the core app.

class Home(models.Model):
    parent = models.OneToOneField(User, primary_key=True,  # used as primary key as each parent should only have 1 home.
                                  help_text='The parent user for whom the home is defined.')
    children = models.ManyToManyField(User, related_name='homes_enrolled_set',
                                      help_text='The set of student users managed by the parent of this home.')

    def __unicode__(self):
        return unicode('%s %s\'s Home' % (self.parent.first_name, self.parent.last_name))


class School(models.Model):
    # NOTE: name is not unique=True as the same school name with differing board can be used for schools that have multiple curriculums
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, help_text='Full name of the school. Must be unique.')
    board = models.ForeignKey(Board, help_text='The board/curriculum that this school follows.')
    admin = models.OneToOneField(User, help_text='The admin user who manages this school.')

    def __unicode__(self):
        return unicode('%s (%s)' % (self.name, self.board.name))


class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True, help_text='The user object that this info is associated with.')
    group = models.ForeignKey(Group, help_text='Please select the type of user account to be created.')
    school = models.ForeignKey(School,
                               help_text='Please select the school that this user belongs to.')  # slightly redundant, but reduces query complexity

    def __unicode__(self):
        return unicode('%s %s\'s Info' % (self.user.first_name, self.user.last_name))


class ClassRoom(models.Model):
    school = models.ForeignKey(School, help_text='The school that this classroom belongs to.')
    standard = models.ForeignKey(Standard, help_text='The standard of this classroom.')
    division = models.CharField(max_length=MAX_CHARFIELD_LENGTH,
                                help_text='The division name of this classroom, as a string.')
    # Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
    classTeacher = models.ForeignKey(User, related_name='classes_managed_set',
                                     help_text='The teacher user managing this classroom.')
    # in truth though this should just be oneToMany with student
    students = models.ManyToManyField(User, related_name='classes_enrolled_set',
                                      help_text='The set of student users in this classroom.')

    def __unicode__(self):
        return unicode('%s - STD %u - DIV %s' % (self.school.__unicode__(), self.standard.number, self.division))


class Question(models.Model):
    # Question can belong to single-school or a shared-school (HWCentralRepo)
    school = models.ForeignKey(School,
                               help_text='The school question bank that this question belongs to. Use 1 if it belongs to the hwcentral question bank.')
    standard = models.ForeignKey(Standard, help_text='The standard that this question is for.')
    subject = models.ForeignKey(Subject, help_text='The subject that this question is for.')
    chapter = models.ForeignKey(Chapter, help_text='The chapter that this question pertains to.')
    tags = models.ManyToManyField(QuestionTag,
                                  help_text='The set of question tags that this question has been tagged with.')

    def __unicode__(self):
        return unicode('STD %s - %s - %s - %u' % (self.standard.number, self.subject.name, self.chapter.name, self.pk))


## A simple representation of the question subpart in the database. DO NOT couple tightly with cabinet representation
class QuestionSubpart(models.Model):
    tags = models.ManyToManyField(QuestionTag,
                                  help_text='The set of question tags that this subpart has been tagged with.')
    question = models.ForeignKey(Question, help_text='The question that this subpart belongs to.')
    index = models.PositiveIntegerField(
        help_text='The index of this subpart in the ordering of all subparts for its parent question.')


class AssignmentQuestionsList(models.Model):
    questions = models.ManyToManyField(Question, help_text='The set of questions that make up an assignment.')
    # AQL can belong to a single-school or a shared-school (HWCentralRepo)
    school = models.ForeignKey(School,
                               help_text='The school that this Assignment Questions List belongs to. Use 1 if it belongs to the hwcentral question bank')
    standard = models.ForeignKey(Standard, help_text='The standard that this Assignment Questions List is for.')
    subject = models.ForeignKey(Subject, help_text='The subject that this Assignment Questions List is for.')
    number = models.PositiveIntegerField(
        help_text='A positive integer used to disinguish Assignment Questions List for the same chapter.')
    chapter = models.ForeignKey(Chapter, help_text='The Chapter that this Assignment Questions List pertains to.')
    description = models.TextField(max_length=MAX_TEXTFIELD_LENGTH,
                                   help_text='A brief description/listing of the topics covered by this Assignment Question List.')

    def __unicode__(self):
        return unicode('%s - %s - %s - %s' % (self.school.pk, self.standard, self.subject, self.get_title()))

    def get_title(self):
        return unicode("%s - %u" % (self.chapter.name, self.number))


class Assignment(models.Model):
    limit = (models.Q(app_label=CORE_APP_LABEL) & models.Q(model='subjectroom')) \
            | (models.Q(app_label='focus') & models.Q(model='remedial')) \
            | (models.Q(app_label='auth') & models.Q(model='user'))
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit,
                                     help_text='The type of the target of this assignment.')
    object_id = models.PositiveIntegerField(help_text='The primary key of the target of this assignment.')
    content_object = GenericForeignKey()  # picks up content_type and object_id by default

    assignmentQuestionsList = models.ForeignKey(AssignmentQuestionsList,
                                                help_text='The list of questions that make up this assignment.')
    assigned = models.DateTimeField(help_text='Timestamp of when this assignment was assigned.')
    due = models.DateTimeField(help_text='Timestamp of when this assignment is due.')
    average = models.FloatField(null=True, blank=True, help_text='Subjectroom average (fraction) for this assignment.',
                                validators=FRACTION_VALIDATOR)
    completion = models.FloatField(null=True, blank=True,
                                   help_text='Completion rate (fraction) over the entire subjectroom for this assignment.',
                                   validators=FRACTION_VALIDATOR)
    number = models.PositiveIntegerField(
        help_text='A positive integer used to disinguish Assignments using the same AssignmentQuestionsList in the same subjectroom.')

    def __unicode__(self):
        return unicode('%s - ASN %u' % (self.content_object.__unicode__(), self.pk))

    def get_title(self):
        if self.number == 0:
            return self.assignmentQuestionsList.get_title()
        return unicode('%s (%s)' % (self.assignmentQuestionsList.get_title(), chr(self.number + 64)))

    def get_subjectroom(self):
        from focus.models import Remedial
        if self.content_type == ContentType.objects.get_for_model(SubjectRoom):
            return self.content_object
        elif self.content_type == ContentType.objects.get_for_model(Remedial):
            return self.content_object.focusRoom.subjectRoom
        elif self.content_type == ContentType.objects.get_for_model(User):
            raise NotImplementedError('Cannot extract subjectroom for user-targeted assignment.')
        else:
            raise InvalidContentTypeError(self.content_type)

    def get_classroom(self):
        from focus.models import Remedial
        if self.content_type == ContentType.objects.get_for_model(SubjectRoom):
            return self.content_object.classRoom
        elif self.content_type == ContentType.objects.get_for_model(Remedial):
            return self.content_object.focusRoom.subjectRoom.classRoom
        elif self.content_type == ContentType.objects.get_for_model(User):
            return self.content_object.classes_enrolled_set.get()
        else:
            raise InvalidContentTypeError(self.content_type)

    @classmethod
    def get_new_assignment_number(cls, assignment_questions_list, subjectroom):
        return cls.objects.filter(subjectRoom=subjectroom,
                                  assignmentQuestionsList=assignment_questions_list).count() + cls.objects.filter(
            remedial__focusRoom__subjectRoom=subjectroom, assignmentQuestionsList=assignment_questions_list).count()

    @classmethod
    def get_new_practice_number(cls, assignment_questions_list, student):
        return cls.objects.filter(content_type=ContentType.objects.get_for_model(User), object_id=student.pk,
                                  assignmentQuestionsList=assignment_questions_list).count()


class SubjectRoom(models.Model):
    classRoom = models.ForeignKey(ClassRoom, help_text='The classroom that this subjectroom belongs to.')
    subject = models.ForeignKey(Subject, help_text='The subject that is taught in this subjectroom.')
    # Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
    teacher = models.ForeignKey(User, related_name='subjects_managed_set',
                                help_text='The teacher user teaching this subjectroom.')
    # technically you can get all students that should be in this subjectroom via the classroom, but maintaining list of
    # students for subjectroom for cases like 3rd language / elective
    students = models.ManyToManyField(User, related_name='subjects_enrolled_set',
                                      help_text='The set of student users in this subjectroom.')

    assignments = GenericRelation(Assignment, related_query_name='subjectRoom')

    def __unicode__(self):
        return unicode('%s - %s' % (self.classRoom.__unicode__(), self.subject.name))


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, help_text='The assignment that this submission is for.')
    student = models.ForeignKey(User, help_text='The student user responsible for this submission.')
    marks = models.FloatField(null=True, blank=True, help_text='Marks (fraction) obtained by this submission.',
                              validators=FRACTION_VALIDATOR)
    timestamp = models.DateTimeField(help_text='Timestamp of when this submission was submitted.')
    completion = models.FloatField(help_text='Completion (fraction) of this submission.', validators=FRACTION_VALIDATOR)

    def __unicode__(self):
        return unicode('%s - SUB %u' % (self.assignment.__unicode__(), self.pk))


class Announcement(models.Model):
    limit = models.Q(app_label=CORE_APP_LABEL) & \
            (models.Q(model='school') | models.Q(model='classroom') | models.Q(model='subjectroom'))
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit,
                                     help_text='The type of the target of this announcement.')
    object_id = models.PositiveIntegerField(help_text='The primary key of the target of this announcement.')
    content_object = GenericForeignKey()  # picks up content_type and object_id by default
    message = models.TextField(max_length=MAX_TEXTFIELD_LENGTH,
                               help_text='The textual message to be conveyed to the target.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='Timestamp of when this announcement was issued.')
    announcer = models.ForeignKey(User, help_text='The user who made this announcement')

    def __unicode__(self):
        return unicode('%s - Announcement %u' % (self.content_object.__unicode__(), self.pk))

    def get_target_label(self):
        if self.content_type == ContentType.objects.get_for_model(School):
            return self.content_object.name
        elif self.content_type == ContentType.objects.get_for_model(ClassRoom):
            return get_classroom_label(self.content_object)
        elif self.content_type == ContentType.objects.get_for_model(SubjectRoom):
            return get_subjectroom_label(self.content_object)
        else:
            raise InvalidContentTypeError(self.content_type)

    def get_source_label(self):
        if is_hwcentral_team_admin(self.announcer):
            return 'Homework Central Team'
        return get_user_label(self.announcer)
