from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, BooleanField, Select

from core.forms.fields import TEXTINPUT_MAX_LENGTH, CustomLabelModelChoiceField
from core.models import ClassRoom
from core.utils.labels import get_classroom_label


def validate_name(value):
    value = value.strip()
    if not (value.isalpha() and value.islower()):
        raise ValidationError('%s is not a lowercase alphabetic string' % value)


def validate_mobile_number(value):
    if not (len(value) == PrimaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH and value.isdigit()):
        raise ValidationError('%s is not a valid 10 digit mobile number' % value)
    if value[0] == '0':
        raise ValidationError('%s - mobile numbers cannot begin with 0' % value)


def validate_mobile_or_landline_number(value):
    try:
        validate_mobile_number(value)
    except ValidationError as v:
        value_parts = value.split('-')
        value_clean = ''.join(value_parts)
        if (len(value) != SecondaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH) or (len(value_parts) != 2):
            raise v

        if (len(value_parts[0]) != 2) or (value_parts[0][0] != '0') or (
        not value_clean.isdigit()):
            raise ValidationError('%s is not a valid landline number of the form 020-22222222' % value)


class PhoneNumberField(CharField):
    PHONE_NUMBER_MIN_LENGTH = 10


class PrimaryPhoneNumberField(PhoneNumberField):
    PHONE_NUMBER_MAX_LENGTH = 10

    def __init__(self, **kwargs):
        super(PrimaryPhoneNumberField, self).__init__(
            max_length=PrimaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH,
            min_length=PrimaryPhoneNumberField.PHONE_NUMBER_MIN_LENGTH,
            validators=[validate_mobile_number],
            **kwargs
        )


class SecondaryPhoneNumberField(PhoneNumberField):
    PHONE_NUMBER_MAX_LENGTH = 12

    def __init__(self, **kwargs):
        super(SecondaryPhoneNumberField, self).__init__(
            max_length=SecondaryPhoneNumberField.PHONE_NUMBER_MAX_LENGTH,
            min_length=SecondaryPhoneNumberField.PHONE_NUMBER_MIN_LENGTH,
            validators=[validate_mobile_or_landline_number],
            **kwargs
        )

class BasicNameField(CharField):
    def __init__(self, **kwargs):
        super(BasicNameField, self).__init__(max_length=TEXTINPUT_MAX_LENGTH, validators=[validate_name], **kwargs)


class InkForm(Form):
    fname = BasicNameField(label="First Name (lowercase)", help_text="Enter the student's first name in lower case")
    lname = BasicNameField(label="Last Name (lowercase)", help_text="Enter the student's last name in lower case")

    email = EmailField(label="Primary Email", help_text="Enter the student's primary contact email")

    secondaryEmail = EmailField(required=False, label="Secondary Email (optional)",
                                help_text="Enter the student's secondary contact email")
    phone = PrimaryPhoneNumberField(label="Primary Phone",
                                    help_text="Enter the student's or their parent's 10 digit mobile phone number")
    secondaryPhone = SecondaryPhoneNumberField(label="Secondary Phone (optional)", required=False,
                                               help_text="Enter the student's secondary contact phone number - e.g. 9999999999 (mobile) or 020-22222222 (landline)")

    flagged = BooleanField(required=False, label="Access Problems?",
                           help_text="Check this if the user conveys any problems with computer access at home. Such cases will be prioritized for follow-up")

    def __init__(self, *args, **kwargs):
        super(InkForm, self).__init__(*args, **kwargs)
        self.fields['section'] = CustomLabelModelChoiceField(get_classroom_label, queryset=ClassRoom.objects.all(),
                                                             widget=Select(attrs={'class': 'chosen-select'}),
                                                             help_text="Select the user's section", label="Section",
                                                             empty_label=None)

class ParentForm(Form):
    fname = BasicNameField(label="First Name (lowercase)", help_text="Enter the parent's first name in lower case")
    lname = BasicNameField(label="Last Name (lowercase)", help_text="Enter the parent's last name in lower case")

    email = EmailField(label="Primary Email", help_text="Enter the parent's primary contact email")
    phone = PrimaryPhoneNumberField(label="Primary Phone", help_text="Enter the parent's 10 digit mobile phone number")
