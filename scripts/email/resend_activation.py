import argparse

from django.contrib.auth.models import User

from scripts.email.hwcentral_users import runscript_args_workaround
from scripts.setup.full_school import send_activation_email


def run(*args):
    parser = argparse.ArgumentParser(description="Resend the activation email for a user")

    parser.add_argument('--actual', '-a', action='store_true', help='actually send emails')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--emails', '-e', nargs="+",
                        help='list of email addresses to which the activation email is to be sent again. Users with these emails must exist in database')
    group.add_argument('--late', '-l', action='store_true',
                       help='resend activation emails to all users that have not logged in yet')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    if processed_args.late:
        users = User.objects.filter(last_login__isnull=True)
    else:
        users = []
        for email in processed_args.emails:
            users.append(User.objects.get(email=email))

    resend_activation_emails(users, processed_args.actual)


def resend_activation_emails(users, actual):
    print 'Activation email will be resent to these users: ', users

    for user in users:
        if actual:
            send_activation_email(user.email)
        else:
            print "Skipping email sending for dry run"
