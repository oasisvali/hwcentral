import argparse

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from hwcentral import settings
from scripts.email.hwcentral_users import runscript_args_workaround
from scripts.setup.full_school import SUBJECT_TEMPLATE_NAME, TEXT_BODY_TEMPLATE_NAME, \
    HTML_BODY_TEMPLATE_NAME


def run(*args):
    parser = argparse.ArgumentParser(description="Resend the activation email for a user")
    parser.add_argument('--emails', '-e', required=True, nargs="+",
                        help='list of email addresses to which the activation email is to be sent again. Users with these emails must exist in database')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    users = []
    for email in processed_args.emails:
        users.append(User.objects.get(email=email))

    print 'Activation email will be sent to these users: ', users
    print 'Press Enter to continue...'
    raw_input()

    for user in users:
        form = PasswordResetForm({'email':user.email})
        if form.is_valid():
            print "Sending activation email to user:", user
            opts = {
                'from_email': settings.DEFAULT_FROM_EMAIL,
                'email_template_name': TEXT_BODY_TEMPLATE_NAME,
                'html_email_template_name': HTML_BODY_TEMPLATE_NAME,
                'subject_template_name': SUBJECT_TEMPLATE_NAME,
            }
            form.save(**opts)
            print "Email sent"
        else:
            raise ValidationError('Invalid PasswordResetForm for email %s' % form.email)
