import csv
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from core.models import UserInfo, Group, School
import hwcentral.settings as settings

post_reset_redirect = '/forgot_password/mailed/'
template_name = 'password/forgot_password_form.html'
email_template_name = '/home/hrishikesh/hwcentral/core/templates/activation/activation_email_body.html'
subject_template_name = '/home/hrishikesh/hwcentral/core/templates/activation/activation_email_subject.html'

SETUP_PASSWORD = "gKBuiGurx9k2j7BDIq5JYkkamK4"

def run():
    print settings.DEBUG
    with open('/home/hrishikesh/hwcentral/scripts/setup/test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['email']
            fname = row['fname']
            lname = row['lname']
            group = row['group']
            school = row ['school']
            user = User.objects.create_user(username=fname+lname,
                                     email=email,
                                     password=SETUP_PASSWORD)
            userinfo = UserInfo(user=user)
            userinfo.group_id=group
            userinfo.school_id=school
            userinfo.save()
            form = PasswordResetForm({'email':email})
            print "here"
            print email
            print form.is_valid()
            print form.errors.as_data()
            print form.is_bound
            if form.is_valid():
                opts = {
                        'use_https': False,
                        'token_generator': PasswordResetTokenGenerator(),
                        'from_email': settings.DEFAULT_FROM_EMAIL,
                        'email_template_name': email_template_name,
                        'subject_template_name': subject_template_name,
                        'html_email_template_name': None,
                }
                form.save(**opts)
                print "done"
            print "saved!"
