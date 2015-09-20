# to use this script, run following command from the terminal
# python manage.py runscript scripts.email.hwcentral_users -v3 [--script-args=[-s school_id] [-f parent teacher]]

# description
#
# no args - email all users

# Following can be AND-ed (filters)
# -s school_id :- email only users belonging to school
# -g group :- filter by user group
# -c classroom_id :- email only users belonging to classroom
# -r subjectroom_id :- email only users belonging to subjectroom
# -h home_id :- email only users belonging to home
# -t standard_id :- email only users belonging to standard
# -u username :-filter by username

import argparse
import os
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.template import Template, Context
from core.models import ClassRoom, SubjectRoom, Home
from django.contrib.sites.models import Site
from hwcentral import settings

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hwcentral_users_data')
EMAIL_SUBJECT_FILE = os.path.join(DATA_DIR, 'subject.html')
EMAIL_BODY_FILE = os.path.join(DATA_DIR, 'body.html')


def update_filters_for_classroom(all_filters, classroom):
    valid_users = list(classroom.students.all().values_list('pk', flat=True))
    valid_users.append(classroom.classTeacher.pk)
    all_filters.append(Q(pk__in=valid_users))


def send_actual_email(selected_users):
    with open(EMAIL_SUBJECT_FILE) as f:
        subject = f.read().strip()
    with open(EMAIL_BODY_FILE) as f:
        body = f.read().strip()

    print 'Sending mass email with subject:', subject
    print 'And body:'
    print body

    raw_input('Press any key to continue...')

    site = Site.objects.get(pk=settings.SITE_ID)
    subject_template = Template(subject)
    body_template = Template(body)
    datatuple = ()
    for user in selected_users:
        context = Context({
            'site': site,
            'user': user
        })
        datatuple += ((subject_template.render(context),body_template.render(context),settings.SERVER_EMAIL,[user.email]),)

    print 'Sending mass mail'
    send_mass_mail(datatuple)


def run(*args):
    argv = []
    assert len(args) == 1   # args must be provided to this script as a string
    for arg in args[0].split():
        if arg != '':
            argv.append(arg.replace('#', '-'))  # hacky workaround to get runscript and argparse to cooperate

    parser = argparse.ArgumentParser(description="Email some HWCentral users")
    parser.add_argument('--schools', '-s', nargs="*", type=long, help="list of school ids that emailed users must belong to")
    parser.add_argument('--groups', '-g', nargs="*", help="list of group types that emailed users must belong to")
    parser.add_argument('--classrooms', '-c', nargs="*", type=long, help="list of classroom ids that emailed users must belong to")
    parser.add_argument('--subjectrooms', '-r', nargs="*", type=long, help="list of subjectroom ids that emailed users must belong to")
    parser.add_argument('--homes', '-m', nargs="*", type=long, help="list of home ids that emailed users must belong to")
    parser.add_argument('--standards', '-t', nargs="*", type=int, help="list of standards that emailed users must belong to")
    parser.add_argument('--usernames', '-u', nargs="*", help="list of usernames to email")

    parser.add_argument('--actual', '-a', action='store_true',help='actually send emails' )

    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    all_filters = []

    if processed_args.schools:   # check for None or empty list
        for school_id in processed_args.schools:
            all_filters.append(Q(userinfo__school__pk=school_id))

    if processed_args.groups:   # check for None or empty list
        for group in processed_args.groups:
            all_filters.append(Q(userinfo__group__name=group))

    if processed_args.classrooms:   # check for None or empty list
        for classroom_id in processed_args.classrooms:
            update_filters_for_classroom(all_filters, ClassRoom.objects.get(pk=classroom_id))

    if processed_args.subjectrooms:   # check for None or empty list
        for subjectroom_id in processed_args.subjectrooms:
            subjectroom = SubjectRoom.objects.get(pk=subjectroom_id)
            valid_users = list(subjectroom.students.all().values_list('pk', flat=True))
            valid_users.append(subjectroom.teacher.pk)
            all_filters.append(Q(pk__in=valid_users))

    if processed_args.homes:   # check for None or empty list
        for home_id in processed_args.homes:
            home = Home.objects.get(pk=home_id)
            valid_users = list(home.children.all().values_list('pk', flat=True))
            valid_users.append(home.parent.pk)
            all_filters.append(Q(pk__in=valid_users))

    if processed_args.standards:
        for standard in processed_args.standards:
            for classroom in ClassRoom.objects.filter(standard__number=standard):
                update_filters_for_classroom(all_filters, classroom)

    if processed_args.usernames:
        for username in processed_args.usernames:
            all_filters.append(Q(username=username))

    user_selection_query = Q()
    for filter in all_filters:
        user_selection_query = user_selection_query & filter
    print 'Filters compiled'

    selected_users = list(User.objects.filter(user_selection_query))

    print 'Following users were selected for sending email:'
    for user in selected_users:
        print '\t', user.username

    if not processed_args.actual:
        print 'Dummy run done.'
        return

    send_actual_email(selected_users)
    print 'Done.'








