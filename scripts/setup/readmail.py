import csv
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from core.models import UserInfo, Group, School, Home, SubjectRoom, ClassRoom, Subject, Standard
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
            username = row['username']
            lname = row['lname']
            group = row['group']
            school = row ['school']
            print "creating user : "+fname+lname+" ,email: "+email
            user = User.objects.create_user(username=username,
                                     email=email,
                                     password=SETUP_PASSWORD)
            user.first_name = fname
            user.lat_name = lname
            user.save()
            userinfo = UserInfo(user=user)
            userinfo.group_id=group
            userinfo.school_id=school
            userinfo.save()
            form = PasswordResetForm({'email':email})
            if form.is_valid():
                print "sending email to created user!"
                opts = {
                        'use_https': False,
                        'token_generator': PasswordResetTokenGenerator(),
                        'from_email': settings.DEFAULT_FROM_EMAIL,
                        'email_template_name': email_template_name,
                        'subject_template_name': subject_template_name,
                        'html_email_template_name': None,
                }
                form.save(**opts)
                print "mail sent"

    print "all users saved!"


    with open('/home/hrishikesh/hwcentral/scripts/setup/home.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent = row['parent']
            student = row['student']
            student = student.split(',')
            home = Home()
            print "adding home for parent : "+ str(parent)+" and kids: "+str(student)+" ."
            home.parent =User.objects.get(username = parent)
            for element in student:
                home.students.add(User.objects.get(username = element))
            home.save()
    print "added home for all students"

    with open('/home/hrishikesh/hwcentral/scripts/setup/classroom.csv') as csvfile:
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
            classroomadd.school =School.objects.get(name = school)
            classroomadd.standard =Standard.objects.get(number = standard)
            classroomadd.division = division
            classroomadd.save()
            for element in students:
                classroomadd.students.add(User.objects.get(username = element))
            classroomadd.save()
    print "added classroom for all students and teachers"

    with open('/home/hrishikesh/hwcentral/scripts/setup/subjectroom.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teacher = row['teacher']
            subject = row['subject']
            standard = row['standard']
            division = row['division']
            students = row['students']
            school = row['school']
            students = students.split(',')
            subjectadd = SubjectRoom()
            print "adding subject for teacher : "+ str(teacher) +" Subject : "+str(subject)+str(standard)+str(division)+" ."
            subjectadd.teacher =User.objects.get(username = teacher)
            subjectadd.subject= Subject.objects.get(name = subject)
            standard_element = Standard.objects.filter(number = standard)
            for standards in standard_element:
                try:
                    subjectadd.classRoom=ClassRoom.objects.get(standard=standards,division=division,school=School.objects.get(name =school))
                except:
                    pass
            subjectadd.save()
            for element in students:
                subjectadd.students.add(User.objects.get(username = element))
            subjectadd.save()
    print "added subjectroom for all students and teachers"

