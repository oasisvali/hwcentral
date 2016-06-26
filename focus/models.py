from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import SubjectRoom, Assignment


# TODO: this is a redundant model, remedial can point directly to subjectroom
class FocusRoom(models.Model):
    subjectRoom = models.OneToOneField(SubjectRoom, primary_key=True,
                                       help_text="The subjectroom that this focusroom is for")

    def __unicode__(self):
        return unicode('%s - Focus' % self.subjectRoom.__unicode__())


@receiver(post_save, sender=SubjectRoom)
def create_focusroom(sender, instance, created, **kwargs):
    if created:
        FocusRoom.objects.create(subjectRoom=instance)


class Remedial(models.Model):
    focusRoom = models.ForeignKey(FocusRoom, help_text="The focusroom that this remedial is assigned to")
    students = models.ManyToManyField(User, related_name='remedials_enrolled_set',
                                      help_text='The set of students that have been assigned this remedial')
    assignments = GenericRelation(Assignment, related_query_name='remedial')

    def __unicode__(self):
        return unicode("%s Remedial - %s" % (self.focusRoom, self.pk))
