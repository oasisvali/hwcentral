from django.db import models
from django.contrib.auth.models import User
from hwcentral.settings import ASSIGNMENTS_ROOT, SUBMISSIONS_ROOT, QUESTIONS_ROOT

# NOTE: DJANGO ADDS AUTO-INCREMENTING PRIMARY KEY TO MODELS AUTOMATICALLY WHEN NO PRIMARY KEY HAS BEEN DEFINEED
#	    THESE PRIMARY KEYS ARE ACCESSIBLE AS 'id' ATTRIBUTE

MAX_CHARFIELD_LENGTH = 255    # Applying this limit to allow safely marking any CharField as unique. For longer requirement use TextField
CONFIG_FILE_MATCH = r'\d+\.xml'

# BASIC MODELS - These are used as simple id-name key-value pairs

class Group(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH)

class Board(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH)

class Subject(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH)


class Chapter(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH)

# COMPLEX MODELS - These form the basis of the core app. School, Classroom, UserInfo, Assignment, Topic, Submission

class Home(models.Model):
    parent = models.ForeignKey(User, primary_key=True,
                               related_name='homes_managed_set')  # used as primary key as each parent should only have 1 home
    children = models.ManyToManyField(User, related_name='homes_enrolled_set')


class School(models.Model):
    name = models.CharField(unique=True, max_length=MAX_CHARFIELD_LENGTH)
    board = models.ForeignKey(Board)
    admin = models.ForeignKey(User)

class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    group = models.ForeignKey(Group)
    school = models.ForeignKey(School)  # slightly redundant, but reduces query complexity


class ClassRoom(models.Model):
    school = models.ForeignKey(School)
    standard = models.PositiveIntegerField()
    division = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    # Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
    classTeacher = models.ForeignKey(User, related_name='classes_managed_set')
    students = models.ManyToManyField(User, related_name='classes_enrolled_set')


class SubjectRoom(models.Model):
    classRoom = models.ForeignKey(ClassRoom)
    subject = models.ForeignKey(Subject)
    # Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
    teacher = models.ForeignKey(User, related_name='subjects_managed_set')
    students = models.ManyToManyField(User, related_name='subjects_enrolled_set')


class Question(models.Model):
    school = models.ForeignKey(School)
    standard = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject)
    chapter = models.ForeignKey(Chapter)
    conf = models.FilePathField(path=QUESTIONS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH)


class Assignment(models.Model):
    questions = models.ManyToManyField(Question)
    chapter = models.ForeignKey(Chapter)
    subjectRoom = models.ForeignKey(SubjectRoom)
    created = models.DateTimeField(auto_now_add=True)
    assigned = models.DateTimeField()
    due = models.DateTimeField(null=True)
    conf = models.FilePathField(path=ASSIGNMENTS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(User)
    marks = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completion = models.FloatField()
    path = models.FilePathField(path=SUBMISSIONS_ROOT, max_length=MAX_CHARFIELD_LENGTH, match=CONFIG_FILE_MATCH)