# to use this script, run following command from the terminal
# python manage.py runscript scripts.database.enforcer -v3

## THIS IS A READ-ONLY SCRIPT
import json
import os

import django
from django.contrib.auth.models import User

from core.models import Group, Board, Subject, Chapter, QuestionTag, UserInfo, Home, Announcement, School, \
    SubjectRoom, Question, AssignmentQuestionsList, Submission, ClassRoom, Assignment
from core.utils.references import HWCentralGroup, HWCentralRepo
from hwcentral.exceptions import InvalidStateError
from scripts.database.enforcer_exceptions import EmptyNameError, InvalidRelationError, \
    UnsupportedQuestionConfigurationError, UnsupportedAqlConfigurationError, UserNameError, MissingUserInfoError, \
    InvalidHWCAdminError, InvalidHWCAdminUsernameError, UnconfiguredTeacherError, \
    InvalidClassTeacherSchoolError, InvalidSubjectTeacherSchoolError, UnconfiguredParentError, StudentClassroomError, \
    StudentSubjectroomError, InvalidClassStudentSchoolError, InvalidSubjectStudentClassroomError, \
    FutureAnnouncementError, \
    EmptyHomeError, InvalidHomeChildGroupError, HomeSchoolError, InvalidHomeParentGroupError, \
    InvalidSchoolAdminGroupError, \
    EmptySchoolError, InvalidClassTeacherGroupError, InvalidClassStudentGroupError, ClassroomNoStudentsError, \
    ClassroomNoSubjectroomsError, InvalidSubjectTeacherGroupError, InvalidSubjectStudentGroupError, \
    SubjectroomNoStudentsError, InvalidSubjectStudentSchoolError, InvalidAqlQuestionError, DuplicateAqlIdentifierError, \
    InvalidAssignmentAqlSchoolError, InvalidAssignmentAqlSubjectError, InvalidAssignmentAqlStandardError, \
    AssignmentBadTimestampsError, InvalidSubmissionStudentGroupError, InvalidSubmissionStudentSubjectroomError, \
    FutureSubmissionError, InactiveAssignmentSubmissionError, ClosedAssignmentSubmissionError, IncorrectMarkingError, \
    EnforcerError

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enforcer_config.json'), 'r') as f:
    CONFIG = json.load(f)


## HELPERS

def check_non_empty_name(model, name_attr='name'):
    for object in model.objects.all():
        if getattr(object, name_attr).strip() == '':
            raise EmptyNameError(model, name_attr, object.pk)


def check_no_relation_set(user, set_name):
    relation_set = getattr(user, set_name)
    if relation_set.exists():
        raise InvalidRelationError(user, user.userinfo.group, set_name)


def check_no_related_object(user, object_name):
    if hasattr(user, object_name):
        raise InvalidRelationError(user, user.userinfo.group, object_name)


def check_supported_question(question):
    try:
        CONFIG['supported'][str(question.standard)][str(question.subject.pk)][str(question.chapter.pk)]
    except KeyError:
        raise UnsupportedQuestionConfigurationError(question)


def check_supported_aql(aql):
    try:
        CONFIG['supported'][str(aql.standard)][str(aql.subject.pk)]
    except KeyError:
        raise UnsupportedAqlConfigurationError(aql)


def check_duplicate_aql_identifiers(aql_set):
    aql_identifier_set = set()
    for aql in aql_set:
        aql_identifier = get_aql_uid(aql)
        if aql_identifier in aql_identifier_set:
            raise DuplicateAqlIdentifierError(aql)
        aql_identifier_set.add(aql_identifier)


def get_aql_uid(aql):
    return "%s_%s_%s_%s" % (aql.school.pk, aql.standard.number, aql.subject.pk, aql.get_title())

def run():
    # Group, Board, Subject, Chapter, QuestionTag - name is not empty
    print 'checking model Group'
    check_non_empty_name(Group)

    print 'checking model Board'
    check_non_empty_name(Board)

    print 'checking model Subject'
    check_non_empty_name(Subject)

    print 'checking model Chapter'
    check_non_empty_name(Chapter)

    print 'checking model QuestionTag'
    check_non_empty_name(QuestionTag)

    # User - usernames must be valid
    print 'checking model User'
    for user in User.objects.all():
        if not (user.username.replace('_', '').isalnum() and user.username.islower()):
            raise UserNameError(user)
        # userinfos must exist for all users except root
        if user.username == 'root':
            continue
        try:
            userinfo = user.userinfo
        except UserInfo.DoesNotExist:
            raise MissingUserInfoError(user)

    # the following fields must not be empty
    check_non_empty_name(User, 'first_name')
    check_non_empty_name(User, 'last_name')
    check_non_empty_name(User, 'email')

    # Admin - no classes managed, no subjects managed, no home, no homes enrolled, no classes enrolled, no subjects enrolled, no submission set
    # And only 1 school relationship only for hwcadmin
    print 'checking user Admin'
    for admin in User.objects.filter(userinfo__group=HWCentralGroup.refs.ADMIN):
        check_no_relation_set(admin, 'classes_managed_set')
        check_no_relation_set(admin, 'subjects_managed_set')
        check_no_relation_set(admin, 'classes_enrolled_set')
        check_no_relation_set(admin, 'subjects_enrolled_set')
        check_no_relation_set(admin, 'homes_enrolled_set')
        check_no_relation_set(admin, 'submission_set')

        check_no_related_object(admin, 'home')
        if admin.first_name == 'hwcadmin':
            if admin.school != admin.userinfo.school:
                raise InvalidHWCAdminError(admin, admin.school)
            # check format of non-shadow admin username
            if long(admin.username.split('_')[-1]) != admin.school.pk:
                raise InvalidHWCAdminUsernameError(admin)
        else:
            check_no_related_object(admin, 'school')

    # Teacher - no home, no school, no homes enrolled, no classes enrolled, no subjects enrolled, no submission set
    # either classteacher (classes_managed > 0) or subjectteacher (subjects_managed > 0)
    # school value must match
    print 'checking user Teacher'
    for teacher in User.objects.filter(userinfo__group=HWCentralGroup.refs.TEACHER):
        check_no_relation_set(teacher, 'classes_enrolled_set')
        check_no_relation_set(teacher, 'subjects_enrolled_set')
        check_no_relation_set(teacher, 'homes_enrolled_set')
        check_no_relation_set(teacher, 'submission_set')

        check_no_related_object(teacher, 'home')
        check_no_related_object(teacher, 'school')

        if (not teacher.classes_managed_set.exists()) and (not teacher.subjects_managed_set.exists()):
            raise UnconfiguredTeacherError(teacher)
        for classroom in teacher.classes_managed_set.all():
            if classroom.school != teacher.userinfo.school:
                raise InvalidClassTeacherSchoolError(classroom, teacher)
        for subjectroom in teacher.subjects_managed_set.all():
            if subjectroom.classRoom.school != teacher.userinfo.school:
                raise InvalidSubjectTeacherSchoolError(subjectroom, teacher)

    # Parent - no school, no homes enrolled, no classes enrolled, no subjects enrolled, no submission set, no subjects managed, no classes managed
    # has home
    print 'checking user Parent'
    for parent in User.objects.filter(userinfo__group=HWCentralGroup.refs.PARENT):
        check_no_relation_set(parent, 'classes_enrolled_set')
        check_no_relation_set(parent, 'subjects_enrolled_set')
        check_no_relation_set(parent, 'homes_enrolled_set')
        check_no_relation_set(parent, 'classes_managed_set')
        check_no_relation_set(parent, 'subjects_managed_set')
        check_no_relation_set(parent, 'submission_set')

        check_no_related_object(parent, 'school')

        try:
            home = parent.home
        except Home.DoesNotExist:
            raise UnconfiguredParentError(parent)

    # Student - no school, no subjects managed, no classes managed, no home
    # part of at least one subjectroom, and exactly one classroom
    # school value must match
    print 'checking user Student'
    for student in User.objects.filter(userinfo__group=HWCentralGroup.refs.STUDENT):
        check_no_relation_set(parent, 'classes_managed_set')
        check_no_relation_set(parent, 'subjects_managed_set')

        check_no_related_object(student, 'school')
        check_no_related_object(student, 'home')

        if student.classes_enrolled_set.count() != 1:
            raise StudentClassroomError(student)
        if not student.subjects_enrolled_set.exists():
            raise StudentSubjectroomError(student)

        if student.classes_enrolled_set.get().school != student.userinfo.school:
            raise InvalidClassStudentSchoolError(student.classes_enrolled_set.get(), student)
        for subjectroom in student.subjects_enrolled_set.all():
            if subjectroom.classRoom != student.classes_enrolled_set.get():
                raise InvalidSubjectStudentClassroomError(subjectroom, student)
            if subjectroom.classRoom.school != student.userinfo.school:
                raise InvalidSubjectStudentSchoolError(subjectroom, student)

    # Announcement
    # timestamp is in past
    print 'checking model Announcement'
    for announcement in Announcement.objects.all():
        if announcement.timestamp > django.utils.timezone.now():
            raise FutureAnnouncementError(announcement)

    # Home
    # parent is parent group
    # children are student group
    # num children > 0
    print 'checking model Home'
    for home in Home.objects.all():
        if home.parent.userinfo.group != HWCentralGroup.refs.PARENT:
            raise InvalidHomeParentGroupError(home)
        if not home.children.exists():
            raise EmptyHomeError(home)
        for child in home.children.all():
            if child.userinfo.group != HWCentralGroup.refs.STUDENT:
                raise InvalidHomeChildGroupError(home, child)
        # NOTE: for now we do have requirement that all children + parent belong to same school
        for child in home.children.all():
            if child.userinfo.school != home.parent.userinfo.school:
                HomeSchoolError(home, child)

    #
    # School
    # admin is admin group
    # name is not empty
    # has more than one clasroom
    print 'checking model School'
    for school in School.objects.all():
        if school.admin.userinfo.group != HWCentralGroup.refs.ADMIN:
            raise InvalidSchoolAdminGroupError(school, school.admin)
        if not school.classroom_set.exists():
            raise EmptySchoolError(school)

    check_non_empty_name(School)

    # Classroom
    # classteacher has to be teacher
    # students have to be student
    # num students > 0
    # num subjectrooms > 0
    # school has to match for classteacher and all students
    print 'checking model Classroom'
    for classroom in ClassRoom.objects.all():
        if classroom.classTeacher.userinfo.group != HWCentralGroup.refs.TEACHER:
            raise InvalidClassTeacherGroupError(classroom)
        for student in classroom.students.all():
            if student.userinfo.group != HWCentralGroup.refs.STUDENT:
                raise InvalidClassStudentGroupError(classroom, student)
        if not classroom.students.exists():
            raise ClassroomNoStudentsError(classroom)
        if not classroom.subjectroom_set.exists():
            raise ClassroomNoSubjectroomsError(classroom)
        if classroom.school != classroom.classTeacher.userinfo.school:
            raise InvalidClassTeacherSchoolError(classroom, classroom.classTeacher)
        for student in classroom.students.all():
            if classroom.school != student.userinfo.school:
                raise InvalidClassStudentSchoolError(classroom, student)


    # Subjectroom
    # teacher is teacher
    # students are students
    # a student in a subjectroom also belongs to subjectrooms classroom
    # num students > 0
    # school has to match for subjectteacher and all students
    print 'checking model Subjectroom'
    for subjectroom in SubjectRoom.objects.all():
        if subjectroom.teacher.userinfo.group != HWCentralGroup.refs.TEACHER:
            raise InvalidSubjectTeacherGroupError(subjectroom)
        for student in subjectroom.students.all():
            if student.userinfo.group != HWCentralGroup.refs.STUDENT:
                raise InvalidSubjectStudentGroupError(subjectroom, student)
            if subjectroom.classRoom != student.classes_enrolled_set.get():
                raise InvalidSubjectStudentClassroomError(subjectroom, student)
        if not subjectroom.students.exists():
            raise SubjectroomNoStudentsError(subjectroom)
        if subjectroom.classRoom.school != subjectroom.teacher.userinfo.school:
            raise InvalidSubjectTeacherSchoolError(subjectroom, subjectroom.teacher)
        for student in subjectroom.students.all():
            if subjectroom.classRoom.school != student.userinfo.school:
                raise InvalidSubjectStudentSchoolError(subjectroom, student)

    # Questions - standard-subject-chapter is supported
    print 'checking model Question'
    for question in Question.objects.all():
        check_supported_question(question)

    # Aql
    # all questions have same school, standard, subject as aql
    # all questions have same chapter - for now, this is a requirement
    # no 2 aql with same school, standard, subject, chapter number
    # standard-subject is supported
    # description is not empty
    print 'checking model AssignmentQuestionsList'
    check_non_empty_name(AssignmentQuestionsList, 'description')
    for aql in AssignmentQuestionsList.objects.all():
        check_supported_aql(aql)
        for question in aql.questions.all():
            if question.school != aql.school:
                raise InvalidAqlQuestionError(aql, question, 'school')
            if question.standard != aql.standard:
                raise InvalidAqlQuestionError(aql, question, 'standard')
            if question.subject != aql.subject:
                raise InvalidAqlQuestionError(aql, question, 'subject')

        try:
            aql_title = aql.get_title()  # side-effect: checks that all questions have same chapter and also checks that aql has questions
        except InvalidStateError, e:
            raise EnforcerError(str(e))

    check_duplicate_aql_identifiers(AssignmentQuestionsList.objects.all())


    # Assignment
    # aql subject, school is same as subjectroom subject, school (standard of aql must be <= standard of classroom
    # due > assigned
    print 'checking model Assignment'
    for assignment in Assignment.objects.all():
        if (assignment.subjectRoom.classRoom.school != assignment.assignmentQuestionsList.school) and (
            HWCentralRepo.refs.SCHOOL != assignment.assignmentQuestionsList.school):
            raise InvalidAssignmentAqlSchoolError(assignment, assignment.assignmentQuestionsList)
        if assignment.subjectRoom.subject != assignment.assignmentQuestionsList.subject:
            raise InvalidAssignmentAqlSubjectError(assignment, assignment.assignmentQuestionsList)
        if assignment.subjectRoom.classRoom.standard.number < assignment.assignmentQuestionsList.standard.number:
            raise InvalidAssignmentAqlStandardError(assignment, assignment.assignmentQuestionsList)
        if assignment.assigned >= assignment.due:
            raise AssignmentBadTimestampsError(assignment)

    # Submission
    # student belongs to assignments subjectroom,
    # student is student
    # timestamp must be < due of assignment and > assigned of assignment and in past
    print 'checking model Submission'
    for submission in Submission.objects.all():
        if submission.student.userinfo.group != HWCentralGroup.refs.STUDENT:
            raise InvalidSubmissionStudentGroupError(submission, submission.student)
        if not submission.assignment.subjectRoom.students.filter(pk=submission.student.pk).exists():
            raise InvalidSubmissionStudentSubjectroomError(submission, submission.student)
        if submission.timestamp > django.utils.timezone.now():
            raise FutureSubmissionError(submission)
        if submission.timestamp > submission.assignment.due:
            raise ClosedAssignmentSubmissionError(submission)
        if submission.timestamp < submission.assignment.assigned:
            raise InactiveAssignmentSubmissionError(submission)
        if submission.marks > submission.completion:
            raise IncorrectMarkingError(submission)

    print 'Enforcer reports: All OK'
