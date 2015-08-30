import csv

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

from core.models import UserInfo, Home, SubjectRoom, ClassRoom, Standard
import hwcentral.settings as settings


# to use this script, run following command from the terminal
# python manage.py runscript scripts.setup.full_school -v3
#
# ensure all the csv files mentioned below are in the same
# folder as the script.

EMAIL_TEMPLATE_NAME = 'activation/email_body.html'
SUBJECT_TEMPLATE_NAME = 'activation/email_subject.html'

USER_CSV_PATH = './scripts/setup/user.csv'
HOME_CSV_PATH ='./scripts/setup/home.csv'
CLASSROOM_CSV_PATH ='./scripts/setup/classroom.csv'
SUBJECTROOM_CSV_PATH ='./scripts/setup/subjectroom.csv'

SETUP_PASSWORD = "gKBuiGurx9k2j7BDIq5JYkkamK4"
if settings.DEBUG == False:
    with open('/etc/setup_password.txt', 'r') as f:
        SETUP_PASSWORD = f.read().strip()

def run():
    with open(USER_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['email']
            fname = row['fname']
            username = row['username']
            lname = row['lname']
            group = row['group']
            school = row ['school']
            print "creating user : "+fname+" "+lname+" ,email: "+email
            user = User.objects.create_user(username=username,
                                     email=email,
                                     password=SETUP_PASSWORD)
            user.first_name = fname
            user.last_name = lname
            user.save()
            userinfo = UserInfo(user=user)
            userinfo.group_id=group
            userinfo.school_id=school
            userinfo.save()
            form = PasswordResetForm({'email':email})
            if form.is_valid():
                print "sending email to created user!"
                opts = {
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                    'email_template_name': EMAIL_TEMPLATE_NAME,
                    'subject_template_name': SUBJECT_TEMPLATE_NAME,
                }
                form.save(**opts)
                print "mail sent"

    print "all users saved!"


    with open(HOME_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent = row['parent']
            student = row['student']
            student = student.split(',')
            home = Home()
            print "adding home for parent : "+ str(parent)+" and kids: "+str(student)+" ."
            home.parent =User.objects.get(username = parent)
            for element in student:
                home.children.add(User.objects.get(username=element))
            home.save()
    print "added home for all students"

    with open(CLASSROOM_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            classteacher = row['classteacher']
            school = row['school']
            standard = row['standard']
            students = row['students']
            division =row['division']
            students = students.split(',')
            classroomadd = ClassRoom()
            print "adding classroom for teacher : "+ str(classteacher) +" class : "+str(school)+str(standard)+str(division)+" students : " +\
                  " "+str(students)+" ."
            classroomadd.classTeacher =User.objects.get(username = classteacher)
            classroomadd.school_id = school
            classroomadd.standard =Standard.objects.get(number = standard)
            classroomadd.division = division
            classroomadd.save()
            for element in students:
                classroomadd.students.add(User.objects.get(username = element))
            classroomadd.save()
    print "added classroom for all students and teachers"

    with open(SUBJECTROOM_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teacher = row['teacher']
            subjectid = row['subjectid']
            classroomid = row['classroomid']
            students = row['students']
            students = students.split(',')
            subjectadd = SubjectRoom()
            print "adding subject for teacher : "+ str(teacher) +" Subject : "+str(subjectid)+str(ClassRoom.objects.get(pk=classroomid))+" ."
            subjectadd.teacher =User.objects.get(username = teacher)
            subjectadd.subject_id= subjectid
            subjectadd.classRoom_id= classroomid
            subjectadd.save()
            for element in students:
                subjectadd.students.add(User.objects.get(username = element))
            subjectadd.save()
    print "added subjectroom for all students and teachers"

