from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, BooleanField

from core.forms.fields import TEXTINPUT_MAX_LENGTH, CustomLabelModelChoiceField
from core.models import ClassRoom
from core.utils.labels import get_classroom_label


def validate_name(value):
    value = value.strip()
    if not (value.isalpha() and value.islower()):
        raise ValidationError('%s is not a lowercase alphabetic string' % value)


class BasicPhoneNumberField(CharField):
    PHONE_NUMBER_MAX_LENGTH = 15
    PHONE_NUMBER_MIN_LENGTH = 8

    def __init__(self, **kwargs):
        super(BasicPhoneNumberField, self).__init__(max_length=BasicPhoneNumberField.PHONE_NUMBER_MAX_LENGTH,
                                                    min_length=BasicPhoneNumberField.PHONE_NUMBER_MIN_LENGTH, **kwargs)


class BasicNameField(CharField):
    def __init__(self, **kwargs):
        super(BasicNameField, self).__init__(max_length=TEXTINPUT_MAX_LENGTH, validators=[validate_name], **kwargs)


class InkForm(Form):
    fname = BasicNameField(label="First Name (lowercase)", help_text="Enter the user's first name in lower case")
    lname = BasicNameField(label="Last Name (lowercase)", help_text="Enter the user's last name in lower case")

    email = EmailField(label="Primary Email", help_text="Enter the user's primary contact email")

    secondaryEmail = EmailField(required=False, label="Secondary Email (optional)",
                                help_text="Enter the user's secondary contact email")
    phone = BasicPhoneNumberField(label="Primary Phone", help_text="Enter the user's primary contact phone number")
    secondaryPhone = BasicPhoneNumberField(label="Secondary Phone (optional)", required=False,
                                           help_text="Enter the user's secondary contact phone number")

    flagged = BooleanField(required=False, label="Access Problems?",
                           help_text="Check this if the user conveys any problems with computer access at home. Such cases will be prioritized for follow-up")

    def __init__(self, *args, **kwargs):
        super(InkForm, self).__init__(*args, **kwargs)
        self.fields['section'] = CustomLabelModelChoiceField(get_classroom_label, queryset=ClassRoom.objects.all(),
                                                             help_text="Select the user's section", label="Section",
                                                             empty_label=None)
