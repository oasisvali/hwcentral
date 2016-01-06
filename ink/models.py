from django.contrib.auth.models import User
from django.db import models

from ink.forms import BasicPhoneNumberField


class Dossier(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                help_text='The user object that this dossier is associated with.')

    secondaryEmail = models.EmailField(help_text='Secondary contact email for the user', null=True, blank=True)
    flagged = models.BooleanField(help_text='Is this user flagged for follow-up?')

    phone = models.CharField(max_length=BasicPhoneNumberField.PHONE_NUMBER_MAX_LENGTH,
                             help_text='Primary contact phone number for the user')
    secondaryPhone = models.CharField(max_length=BasicPhoneNumberField.PHONE_NUMBER_MAX_LENGTH, null=True, blank=True,
                                      help_text='Secondary contact phone number for the user')

    def __unicode__(self):
        return unicode("Dossier for %s" % self.user)
