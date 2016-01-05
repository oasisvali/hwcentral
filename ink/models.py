from django.contrib.auth.models import User
from django.db import models

PHONE_NUMBER_MAX_LENGTH = 15
PHONE_NUMBER_MIN_LENGTH = 8


class Dossier(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                help_text='The user object that this dossier is associated with.')

    secondaryEmail = models.EmailField(help_text='Secondary contact email for the user', null=True, blank=True)
    flagged = models.BooleanField(help_text='Is this user flagged for follow-up?')

    phone = models.CharField(max_length=15, min_length=8, help_text='Primary contact phone number for the user')
    secondaryPhone = models.CharField(max_length=15, min_length=8, null=True, blank=True,
                                      help_text='Secondary contact phone number for the user')

    def __unicode__(self):
        return unicode("Dossier for %s" % self.user)
