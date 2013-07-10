from django.db import models
from django.contrib.auth.models import User
from hwcentral.settings import ASSIGNMENTS_ROOT, SUBMISSIONS_ROOT

# NOTE: DJANGO ADDS AUTOINCREMENTING PRIMARY KEY TO MODELS AUTOMATICALLY WHEN NO PRIMARY KEY HAS BEEN DEFINEED
#	    THESE PRIMARY KEYS ARE ACCESSIBLE AS 'id' ATTRIBUTE

MAX_CHARFIELD_LENGTH = 255	# Applying this limit to allow safely marking any CharField as unique. For longer requirement use TextField


# BASIC MODELS - These are used as simple id-name key-value pairs

class Group(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)

class Board(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)

class Subject(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)

class AssignmentType(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)

class ClassAccessLevel(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)

# COMPLEX MODELS - These form the basis of the core app. School, Class, UserInfo, Assignment, Topic, Submission

class School(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)
	board = models.ForeignKey(Board)
	admin = models.ForeignKey(User)
	registered = models.DateTimeField(auto_now_add = True)
	# Using flexible text fields here. Since these are strings, they can be empty strings too for null cases. can be customized in future
	address = models.TextField()
	phone = models.CharField(max_length = MAX_CHARFIELD_LENGTH)

class UserInfo(models.Model):
	user = models.OneToOneField(User)
	group = models.ForeignKey(Group)
	school = models.ForeignKey(School)

class Topic(models.Model):
	name = models.CharField(unique = True, max_length = MAX_CHARFIELD_LENGTH)
	subject = models.ForeignKey(Subject)

class Class(models.Model):
	access = models.ForeignKey(ClassAccessLevel)
	school = models.ForeignKey(School)
	subject = models.ForeignKey(Subject)
	created = models.DateTimeField(auto_now_add = True)
	standard = models.PositiveIntegerField()
	# Since both fields below link to same model, related_name must be specified to prevent conflict in names of their backwards-relations
	teacher = models.ForeignKey(User, related_name = 'classes_managed_set')
	students = models.ManyToManyField(User, related_name = 'classes_enrolled_set')

class Assignment(models.Model):
	topics = models.ManyToManyField(Topic)
	created = models.DateTimeField(auto_now_add = True)
	assigned = models.DateTimeField()
	due = models.DateTimeField(null = True)
	duration = models.TimeField(null = True)
	path = models.FilePathField(unique = True, path = ASSIGNMENTS_ROOT, recursive = True, max_length = MAX_CHARFIELD_LENGTH, match = "assignment_\d+\.xml")
	# Modified names to avoid conflict with built-ins
	_type = models.ForeignKey(AssignmentType)
	_class = models.ForeignKey(Class)

class Submission(models.Model):
	assigment = models.ForeignKey(Assignment)
	student = models.ForeignKey(User)
	grade = models.FloatField(null = True)
	timestamp = models.DateTimeField(auto_now_add = True)
	completion = models.FloatField()
	path = models.FilePathField(unique = True, path = SUBMISSIONS_ROOT, recursive = True, max_length = MAX_CHARFIELD_LENGTH, match = "submission_\d+\.xml")