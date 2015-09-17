from core.utils.assignment import is_assignment_corrected
from core.utils.references import HWCentralGroup


#######
# CONVENTION - is_* are boolean checks; check_* are hard checks i.e. 404 on fail
#######

def is_subjectteacher(subjectteacher):
    """
    Checks if object passed in is a subjectteacher user, otherwise raises 404
    """
    return (subjectteacher.userinfo.group == HWCentralGroup.refs.TEACHER) and subjectteacher.subjects_managed_set.exists()

def is_classteacher(classteacher):
    """
    Checks if object passed in is a classteacher user, otherwise raises 404
    """
    return classteacher.userinfo.group == HWCentralGroup.refs.TEACHER and classteacher.classes_managed_set.exists()

def is_student_classteacher_relationship(student, classteacher):
    return student.classes_enrolled_set.get().classTeacher == classteacher

def is_subjectroom_classteacher_relationship(subjectroom, classteacher):
    return subjectroom.classRoom.classTeacher == classteacher


def is_parent_child_relationship(parent, child):
    return parent.home.children.filter(pk=child.pk).exists()


def is_subjectroom_student_relationship(subjectroom, student):
    return subjectroom.students.filter(pk=student.pk).exists()


def is_classroom_student_relationship(classroom, student):
    return classroom.students.filter(pk=student.pk).exists()

def is_assignment_teacher_relationship(assignment, teacher):
    return is_subjectroom_classteacher_relationship(assignment.subjectRoom, teacher) or (
    assignment.subjectRoom.teacher == teacher)


def is_student_corrected_assignment_relationship(student, assignment):
    """
    Checks if the given student has been assigned the given assignment and if the given assignment is corrected
    """
    return (is_student_assignment_relationship(student, assignment) and is_assignment_corrected(assignment))


def is_student_assignment_relationship(student, assignment):
    """
    Checks if the given student has been assigned the given assignment
    """
    return student.subjects_enrolled_set.filter(pk=assignment.subjectRoom.pk).exists()
