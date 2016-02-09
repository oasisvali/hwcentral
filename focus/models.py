from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.models import SubjectRoom, Assignment, School


class FocusRoom(models.Model):
    subjectRoom = models.OneToOneField(SubjectRoom, primary_key=True,
                                       help_text="The subjectroom that this focusroom is for")

    def __unicode__(self):
        return unicode('%s - Focus' % self.subjectRoom.__unicode__())


class Remedial(models.Model):
    focusRoom = models.ForeignKey(FocusRoom, help_text="The focusroom that this remedial is assigned to")
    students = models.ManyToManyField(User, related_name='remedials_enrolled_set',
                                      help_text='The set of students that have been assigned this remedial')
    assignments = GenericRelation(Assignment, related_query_name='remedial')

    def __unicode__(self):
        return unicode("%s Remedial - %s" % (self.focusRoom, self.pk))


class SchoolProfile(models.Model):
    school = models.OneToOneField(School, primary_key=True, help_text="The school that this focus profile is for")
    focusRoom = models.BooleanField(help_text="Whether the focusroom feature is enabled for this school", default=True)

    def __unicode__(self):
        return unicode("Focus Room %s" % ('enabled' if self.focusRoom else 'disabled'))
