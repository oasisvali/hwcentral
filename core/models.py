from django.db import models
from django.contrib.auth.models import User
from hwcentral.settings import ASSIGNMENTS_ROOT, SUBMISSIONS_ROOT, QUESTIONS_ROOT

# NOTE: DJANGO ADDS AUTO-INCREMENTING PRIMARY KEY TO MODELS AUTOMATICALLY WHEN NO PRIMARY KEY HAS BEEN DEFINEED
#	    THESE PRIMARY KEYS ARE ACCESSIBLE AS 'id' ATTRIBUTE

MAX_CHARFIELD_LENGTH = 255    # Applying this limit to allow safely marking any CharField as unique. For longer requirement use TextField
CONFIG_FILE_MATCH = r'\d+\.xml'

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

# TODO: there will eventually be a requirement for a 'supported' Standard-Subject-Chapter' configuration file.
# Either that or start defining relationships between standard, subject, chapter etc. (Redundant and exponentially growing)

# COMPLEX MODELS - These form the basis of the core app.
class Home(models.Model):
    parent = models.ForeignKey(User, primary_key=True, # used as primary key as each parent should only have 1 home
                               related_name='homes_managed_set',
                               help_text='The parent user for whom the home is defined.')
    children = models.ManyToManyField(User, related_name='homes_enrolled_set',
                                      help_text='The set of student users managed by the parent of this home.')

    def __unicode__(self):
        return unicode('%s %s\'s Home' % (self.parent.first_name, self.parent.last_name))


class School(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, help_text='Full name of the school. Must be unique.')
    board = models.ForeignKey(Board, help_text='The board/curriculum that this school follows.')
    admin = models.ForeignKey(User, help_text='The admin user who manages this school.')

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
    students = models.ManyToManyField(User, related_name='classes_enrolled_set',
                                      help_text='The set of student users in this classroom.')

    def __unicode__(self):
        return unicode('%s - STD %u - DIV %s' % (self.school.__unicode__(), self.standard.number, self.division))


class SubjectRoom(models.Model):
    classRoom = models.ForeignKey(ClassRoom, help_text='The classroom that this subjectroom belongs to.')
    subject = models.ForeignKey(Subject, help_text='The subject that is taught in this subjectroom.')
    # Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
    teacher = models.ForeignKey(User, related_name='subjects_managed_set',
                                help_text='The teacher user teaching this subjectroom.')
    students = models.ManyToManyField(User, related_name='subjects_enrolled_set',
                                      help_text='The set of student users in this subjectroom.')

    def __unicode__(self):
        return unicode('%s - %s' % (self.classRoom.__unicode__(), self.subject.name))


class Question(models.Model):
    school = models.ForeignKey(School,
                               help_text='The school question bank that this question belongs to. Use \'hwcentral\' if it belongs to the global question bank.')
    standard = models.ForeignKey(Standard, help_text='The standard that this question is for.')
    subject = models.ForeignKey(Subject, help_text='The subject that this question is for.')
    chapter = models.ForeignKey(Chapter, help_text='The chapter that this question is for.')
    meta = models.FilePathField(path=QUESTIONS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH,
                                help_text='Path to this question\'s metadata file.')

    def __unicode__(self):
        return unicode('%s - STD %s - %s - %s (%u)' % (
        self.school.__unicode__(), self.standard.number, self.subject.name, self.chapter.name, self.pk))


class Assignment(models.Model):
    questions = models.ManyToManyField(Question, help_text='The set of questions that make up this assignment.')
    subjectRoom = models.ForeignKey(SubjectRoom, help_text='The subjectroom that this assignment belongs to.')
    assigned = models.DateTimeField(help_text='Timestamp of when this assignment was assigned.')
    due = models.DateTimeField(null=True, help_text='Timestamp of when this assignment is due.')
    meta = models.FilePathField(path=ASSIGNMENTS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH,
                                help_text='Path to this assignment\'s metadata file.')

    def __unicode__(self):
        return unicode('%s - ASN %u' % (self.subjectRoom.__unicode__(), self.pk))


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, help_text='The assignment that this submission is for.')
    student = models.ForeignKey(User, help_text='The student user responsible for this submission.')
    marks = models.FloatField(null=True, help_text='Marks (percentage) obtained by this submission.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='Timestamp of when this submission was submitted.')
    completion = models.FloatField(help_text='Completion (percentage) of this submission.')
    meta = models.FilePathField(path=SUBMISSIONS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH,
                                help_text='Path to this submission\'s metadata file.')

    def __unicode__(self):
        return unicode('%s - SUB %u' % (self.assignment.__unicode__(), self.pk))