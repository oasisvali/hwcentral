from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from ink.forms import validate_mobile_number, PrimaryPhoneNumberField, SecondaryPhoneNumberField
from pylon.pylon_api import InvalidPhoneError


class Dossier(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                help_text='The user object that this dossier is associated with.')

    secondaryEmail = models.EmailField(help_text='Secondary contact email for the user', null=True, blank=True)
    flagged = models.BooleanField(help_text='Is this user flagged for follow-up?')

    phone = models.CharField(max_length=PrimaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH,
                             help_text='Primary contact phone number for the user')
    secondaryPhone = models.CharField(max_length=SecondaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH, null=True,
                                      blank=True,
                                      help_text='Secondary contact phone number for the user')

    def __unicode__(self):
        return unicode("Dossier for %s" % self.user)

    def get_sanitized_phone(self):
        """
        Runs basic sanity checks on the primary phone number in a dossier object
        @return: sanitized primary phone number with 91 prefix
        @raise: InvalidPhoneError if the primary phone number in the dossier is malformed
        """

        try:
            validate_mobile_number(self.phone)
        except ValidationError:
            raise InvalidPhoneError(self.user, self.phone)

        return '91' + self.phone
