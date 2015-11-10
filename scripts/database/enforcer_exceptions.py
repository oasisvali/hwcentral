## EXCEPTIONS
from hwcentral.exceptions import InvalidStateError


class EnforcerError(InvalidStateError):
    pass


class EmptyNameError(EnforcerError):
    def __init__(self, model, name_attr, id, *args, **kwargs):
        super(EmptyNameError, self).__init__("Empty %s for object type :%s id: %s" % (name_attr, model.__name__, id))


class InvalidRelationError(EnforcerError):
    def __init__(self, user, group, relation, *args, **kwargs):
        super(InvalidRelationError, self).__init__(
            "Invalid relation %s exists for user %s of group %s" % (relation, user.username, group.name))


class UnsupportedQuestionConfigurationError(EnforcerError):
    def __init__(self, question, *args, **kwargs):
        super(UnsupportedQuestionConfigurationError, self).__init__(
            "Enforcer config does not support question id: %s with standard: %s subject: %s chapter: %s" % (
            question.pk, question.standard.number, question.subject.pk, question.chapter.pk))


class UnsupportedAqlConfigurationError(EnforcerError):
    def __init__(self, aql, *args, **kwargs):
        super(UnsupportedAqlConfigurationError, self).__init__(
            "Enforcer config does not support aql id: %s with standard: %s subject: %s" % (
            aql.pk, aql.standard.number, aql.subject.pk))


class UserNameError(EnforcerError):
    def __init__(self, user, *args, **kwargs):
        super(UserNameError, self).__init__("Invalid username %s for id: %s" % (user.username, user.pk))


class MissingUserInfoError(EnforcerError):
    def __init__(self, user, *args, **kwargs):
        super(MissingUserInfoError, self).__init__("No userinfo found for user %s" % (user.username))


class InvalidHWCAdminError(EnforcerError):
    def __init__(self, hwc_admin, school, *args, **kwargs):
        super(InvalidHWCAdminError, self).__init__("hwcadmin: %s is admin for school: %s but belongs to school: %s" % (
        hwc_admin.username, school.pk, hwc_admin.userinfo.school.pk))


class InvalidHWCAdminUsernameError(EnforcerError):
    def __init__(self, hwc_admin, *args, **kwargs):
        super(InvalidHWCAdminUsernameError, self).__init__(
            "Invalid username: %s for hwcadmin with school id: %s" % (hwc_admin.username, hwc_admin.userinfo.school.pk))


class UnconfiguredTeacherError(EnforcerError):
    def __init__(self, teacher, *args, **kwargs):
        super(UnconfiguredTeacherError, self).__init__("teacher %s manages no classes or subjects" % (teacher.username))


class InvalidClassTeacherSchoolError(EnforcerError):
    def __init__(self, classroom, teacher, *args, **kwargs):
        super(InvalidClassTeacherSchoolError, self).__init__(
            "classteacher %s for classroom: %s in school: %s belongs to school: %s" % (
            teacher.username, classroom.pk, classroom.school.pk, teacher.userinfo.school.pk))


class InvalidSubjectTeacherSchoolError(EnforcerError):
    def __init__(self, subjectroom, teacher, *args, **kwargs):
        super(InvalidSubjectTeacherSchoolError, self).__init__(
            "subjectteacher %s for subjectroom: %s in school: %s belongs to school: %s" % (
            teacher.username, subjectroom.pk, subjectroom.classRoom.school.pk, teacher.userinfo.school.pk))


class UnconfiguredParentError(EnforcerError):
    def __init__(self, parent, *args, **kwargs):
        super(UnconfiguredParentError, self).__init__("parent %s has no home associated" % (parent.username))


class StudentClassroomError(EnforcerError):
    def __init__(self, student, *args, **kwargs):
        super(StudentClassroomError, self).__init__(
            "student %s is enrolled in %i classrooms" % (student.username, student.classes_enrolled_set.count()))


class StudentSubjectroomError(EnforcerError):
    def __init__(self, student, *args, **kwargs):
        super(StudentSubjectroomError, self).__init__(
            "student %s is not enrolled in any subjectrooms" % (student.username))


class InvalidClassStudentSchoolError(EnforcerError):
    def __init__(self, classroom, student, *args, **kwargs):
        super(InvalidClassStudentSchoolError, self).__init__(
            "student %s in classroom: %s in school: %s belongs to school: %s" % (
            student.username, classroom.pk, classroom.school.pk, student.userinfo.school.pk))


class InvalidSubjectStudentClassroomError(EnforcerError):
    def __init__(self, subjectroom, student, *args, **kwargs):
        super(InvalidSubjectStudentClassroomError, self).__init__(
            "student %s in subjectroom: %s in classroom: %s belongs to classroom: %s" % (
            student.username, subjectroom.pk, subjectroom.classRoom.pk, student.classes_enrolled_set.get().pk))


class InvalidSubjectStudentSchoolError(EnforcerError):
    def __init__(self, subjectroom, student, *args, **kwargs):
        super(InvalidSubjectStudentSchoolError, self).__init__(
            "student %s in subjectroom: %s in school: %s belongs to school: %s" % (
            student.username, subjectroom.pk, subjectroom.classRoom.school.pk, student.userinfo.school.pk))


class FutureAnnouncementError(EnforcerError):
    def __init__(self, announcement, *args, **kwargs):
        super(FutureAnnouncementError, self).__init__("announcement %s is made in the future" % (announcement.pk))


class InvalidHomeParentGroupError(EnforcerError):
    def __init__(self, home, *args, **kwargs):
        super(InvalidHomeParentGroupError, self).__init__(
            "parent %s for home %s, is not of group parent" % (home.parent.username, home.pk))


class EmptyHomeError(EnforcerError):
    def __init__(self, home, *args, **kwargs):
        super(EmptyHomeError, self).__init__("home %s has no children" % (home.pk))


class InvalidHomeChildGroupError(EnforcerError):
    def __init__(self, home, child, *args, **kwargs):
        super(InvalidHomeChildGroupError, self).__init__(
            "child %s for home %s, is not of group student" % (child.username, home.pk))


class HomeSchoolError(EnforcerError):
    def __init__(self, home, child, *args, **kwargs):
        super(HomeSchoolError, self).__init__(
            "child %s is part of school: %s, but in home %s, which is part of school: %s" % (
            child.username, child.userinfo.school.pk, home.pk, home.parent.userinfo.school.pk))


class InvalidSchoolAdminGroupError(EnforcerError):
    def __init__(self, school, admin, *args, **kwargs):
        super(InvalidSchoolAdminGroupError, self).__init__(
            "admin %s for school %s, is not of group admin" % (admin.username, school.pk))


class EmptySchoolError(EnforcerError):
    def __init__(self, school, *args, **kwargs):
        super(EmptySchoolError, self).__init__("school %s has no classrooms" % (school.pk))


class InvalidClassTeacherGroupError(EnforcerError):
    def __init__(self, classroom, *args, **kwargs):
        super(InvalidClassTeacherGroupError, self).__init__(
            "classteacher %s for classroom %s, is not of group teacher" % (
            classroom.classTeacher.username, classroom.pk))


class InvalidClassStudentGroupError(EnforcerError):
    def __init__(self, classroom, student, *args, **kwargs):
        super(InvalidClassStudentGroupError, self).__init__(
            "student %s in classroom %s, is not of group student" % (student.username, classroom.pk))


class ClassroomNoStudentsError(EnforcerError):
    def __init__(self, classroom, *args, **kwargs):
        super(ClassroomNoStudentsError, self).__init__("classroom %s has no students" % (classroom.pk))


class ClassroomNoSubjectroomsError(EnforcerError):
    def __init__(self, classroom, *args, **kwargs):
        super(ClassroomNoSubjectroomsError, self).__init__("classroom %s has no subjectrooms" % (classroom.pk))


class InvalidSubjectTeacherGroupError(EnforcerError):
    def __init__(self, subjectroom, *args, **kwargs):
        super(InvalidSubjectTeacherGroupError, self).__init__(
            "subjectteacher %s for subjectroom %s, is not of group teacher" % (
            subjectroom.teacher.username, subjectroom.pk))


class InvalidSubjectStudentGroupError(EnforcerError):
    def __init__(self, subjectroom, student, *args, **kwargs):
        super(InvalidSubjectStudentGroupError, self).__init__(
            "student %s in subjectroom %s, is not of group student" % (student.username, subjectroom.pk))


class SubjectroomNoStudentsError(EnforcerError):
    def __init__(self, subjectroom, *args, **kwargs):
        super(SubjectroomNoStudentsError, self).__init__("subjectroom %s has no students" % (subjectroom.pk))


class InvalidAqlQuestionError(EnforcerError):
    def __init__(self, aql, question, attr, *args, **kwargs):
        super(InvalidAqlQuestionError, self).__init__(
            "aql %s belonging to %s %s contains question %s belonging to %s %s" % (
            aql.pk, attr, getattr(aql, attr).pk, question.pk, attr, getattr(question, attr).pk))


class DuplicateAqlIdentifierError(EnforcerError):
    def __init__(self, aql, other_aql, *args, **kwargs):
        super(DuplicateAqlIdentifierError, self).__init__(
            "Multiple Aql found with identifier: %s : pks -> %s, %s" % (
            aql, aql.pk, other_aql.pk))


class InvalidAssignmentAqlSchoolError(EnforcerError):
    def __init__(self, assignment, aql, *args, **kwargs):
        super(InvalidAssignmentAqlSchoolError, self).__init__("assignment %s of school %s, uses aql %s of school %s" % (
        assignment.pk, assignment.subjectRoom.classRoom.school.pk, aql.pk, aql.school.pk))


class InvalidAssignmentAqlSubjectError(EnforcerError):
    def __init__(self, assignment, aql, *args, **kwargs):
        super(InvalidAssignmentAqlSubjectError, self).__init__(
            "assignment %s for subject %s, uses aql %s for subject %s" % (
            assignment.pk, assignment.subjectRoom.subject.pk, aql.pk, aql.subject.pk))


class InvalidAssignmentAqlStandardError(EnforcerError):
    def __init__(self, assignment, aql, *args, **kwargs):
        super(InvalidAssignmentAqlStandardError, self).__init__(
            "assignment %s for standard %s, uses aql %s for standard %s" % (
            assignment.pk, assignment.subjectRoom.classRoom.standard.number, aql.pk, aql.standard.number))


class AssignmentBadTimestampsError(EnforcerError):
    def __init__(self, assignment, *args, **kwargs):
        super(AssignmentBadTimestampsError, self).__init__(
            "Assignment %s is due before it is assigned" % (assignment.pk))


class InvalidSubmissionStudentGroupError(EnforcerError):
    def __init__(self, submission, student, *args, **kwargs):
        super(InvalidSubmissionStudentGroupError, self).__init__(
            "submitter %s for submission %s, is not of group student" % (student.username, submission.pk))


class InvalidSubmissionStudentSubjectroomError(EnforcerError):
    def __init__(self, submission, student, *args, **kwargs):
        super(InvalidSubmissionStudentSubjectroomError, self).__init__(
            "submitter %s for submission %s, is not in enrolled in the submission's subjectroom" % (
            student.username, submission.pk))


class FutureSubmissionError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(FutureSubmissionError, self).__init__("submission %s was made in the future" % (submission.pk))


class ClosedAssignmentSubmissionError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(ClosedAssignmentSubmissionError, self).__init__(
            "submission %s was made for a closed assignment" % (submission.pk))

class MissingSubmissionMarksError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(MissingSubmissionMarksError, self).__init__(
            "submission %s for corrected assignment has null marks" % (submission.pk))


class UnexpectedSubmissionMarksError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(UnexpectedSubmissionMarksError, self).__init__(
            "submission %s for uncorrected assignment has non-null marks" % (submission.pk))


class InactiveAssignmentSubmissionError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(InactiveAssignmentSubmissionError, self).__init__(
            "submission %s was made for an inactive assignment" % (submission.pk))


class IncorrectMarkingError(EnforcerError):
    def __init__(self, submission, *args, **kwargs):
        super(IncorrectMarkingError, self).__init__("submission %s has marks %s but completion is only %s" % (
        submission.pk, submission.marks, submission.completion))

class OrphanQuestionTagError(EnforcerError):
    def __init__(self, question_tag, *args, **kwargs):
        super(OrphanQuestionTagError, self).__init__("question tag %s does not apply to any questions" % question_tag)

class BadSchoolAdminError(EnforcerError):
    def __init__(self, school, admin, *args, **kwargs):
        super(BadSchoolAdminError, self).__init__("school %s has bad admin %s" % (school, admin))

class InvalidSchoolAnnouncementError(EnforcerError):
    def __init__(self, announcement, *args, **kwargs):
        super(InvalidSchoolAnnouncementError, self).__init__("school-level announcement %s has invalid announcer %s" % (announcement.pk, announcement.announcer))

class InvalidClassroomAnnouncementError(EnforcerError):
    def __init__(self, announcement, *args, **kwargs):
        super(InvalidClassroomAnnouncementError, self).__init__("classroom-level announcement %s has invalid announcer %s" % (announcement.pk, announcement.announcer))

class InvalidSubjectroomAnnouncementError(EnforcerError):
    def __init__(self, announcement, *args, **kwargs):
        super(InvalidSubjectroomAnnouncementError, self).__init__("subjectroom-level announcement %s has invalid announcer %s" % (announcement.pk, announcement.announcer))

class MissingAssignmentAverageError(EnforcerError):
    def __init__(self, assignment, *args, **kwargs):
        super(MissingAssignmentAverageError, self).__init__("corrected assignment %s has null average" % assignment.pk)

class UnexpectedAssignmentAverageError(EnforcerError):
    def __init__(self, assignment, *args, **kwargs):
        super(UnexpectedAssignmentAverageError, self).__init__("uncorrected assignment %s has non-null average" % assignment.pk)


class IncorrectAssignmentAverageError(EnforcerError):
    def __init__(self, assignment, actual_average, *args, **kwargs):
        super(IncorrectAssignmentAverageError, self).__init__("corrected assignment %s has average: %s but should be %s" % (assignment.pk, assignment.average, actual_average))