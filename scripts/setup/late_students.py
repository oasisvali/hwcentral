import argparse
import csv
import os

from django.contrib.auth.models import User

from core.models import UserInfo, ClassRoom, SubjectRoom
from core.utils.references import HWCentralGroup
from scripts.email.hwcentral_users import runscript_args_workaround
from scripts.fixtures.dump_data import snapshot_db
from scripts.setup.full_school import build_username, SETUP_PASSWORD, send_activation_email

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'late_students_data')
USER_CSV_PATH = os.path.join(DATA_DIR, 'student.csv')


def get_subjectrooms(classroom, subjectroom_ids):
    if subjectroom_ids == '*':
        print 'Selected all subjectrooms'
        return classroom.subjectroom_set.all()

    subjectrooms = []

    for subjectroom_id in subjectroom_ids.split(','):
        subjectroom_id = subjectroom_id.strip()
        if subjectroom_id == '':
            continue
        subjectroom = SubjectRoom.objects.get(pk=subjectroom_id, classRoom=classroom)
        subjectrooms.append(subjectroom)

    print 'Processed subjectrooms list: %s' % subjectrooms
    return subjectrooms


def run(*args):
    parser = argparse.ArgumentParser(description="Add students to a school post-setup")
    parser.add_argument('--actual', '-a', action='store_true',
                        help='actually send emails (otherwise only database changes are made)')

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    snapshot_db()

    with open(USER_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['email']
            fname = row['fname']
            lname = row['lname']
            username = build_username(fname, lname)
            classroom = ClassRoom.objects.get(pk=row['classroom'])
            subjectrooms = get_subjectrooms(classroom, row['subjectrooms'])

            print "Creating user : %s ,email: %s" % (username, email)
            student = User.objects.create_user(username=username,
                                               email=email,
                                               password=SETUP_PASSWORD)
            student.first_name = fname
            student.last_name = lname
            student.save()
            userinfo = UserInfo(user=student)
            userinfo.group = HWCentralGroup.refs.STUDENT
            userinfo.school = classroom.school
            userinfo.save()

            if processed_args.actual:
                send_activation_email(email)
            else:
                print "Skipping email sending for dry run"

            # add new student to classroom
            print '\tAdding student as %s student' % classroom
            classroom.students.add(student)
            classroom.save()

            # add new to subjectrooms
            for subjectroom in subjectrooms:
                print '\tAdding student as %s student' % subjectroom
                subjectroom.students.add(student)
                subjectroom.save()

    print "All students saved!"
