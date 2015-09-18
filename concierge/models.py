from django.db import models

from hwcentral.settings import MAX_CHARFIELD_LENGTH

PHONE_CHARFIELD_LENGTH = 15


class Enquirer(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, help_text="Please enter your name.")
    school = models.CharField(max_length=MAX_CHARFIELD_LENGTH, help_text="Please enter your school/organization.")
    email = models.EmailField(max_length=MAX_CHARFIELD_LENGTH, help_text="Please enter your email address.")
    phone = models.CharField(max_length=PHONE_CHARFIELD_LENGTH, null=True, blank=True,
                             help_text="Please enter your contact phone number.")

    def dump_to_email(self):
        return "Name: %s\nSchool: %s\nEmail: %s\nPhone: %s\n\nDB-id: %s" % (
        self.name, self.school, self.email, self.phone, self.pk)
