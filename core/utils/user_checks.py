from core.utils.assignment import is_assignment_corrected, is_corrected_open_assignment


#######
# CONVENTION - is_* are boolean checks; check_* are hard checks i.e. 404 on fail
#######
from core.utils.references import HWCentralGroup


def is_subjectteacher(subjectteacher):
    """
    Checks if object passed in is a subjectteacher user, otherwise raises 404
    """
    from core.utils.references import HWCentralGroup
    return (subjectteacher.userinfo.group == HWCentralGroup.refs.TEACHER) and subjectteacher.subjects_managed_set.exists()

def is_classteacher(classteacher):
    """
    Checks if object passed in is a classteacher user, otherwise raises 404
    """
    from core.utils.references import HWCentralGroup
    return classteacher.userinfo.group == HWCentralGroup.refs.TEACHER and classteacher.classes_managed_set.exists()

def is_student_classteacher_relationship(student, classteacher):
    return student.classes_enrolled_set.get().classTeacher == classteacher


def is_student_subjectteacher_relationship(student, subjectteacher):
    return student.subjects_enrolled_set.filter(teacher=subjectteacher).exists()

def is_subjectroom_classteacher_relationship(subjectroom, classteacher):
    return subjectroom.classRoom.classTeacher == classteacher


def is_parent_child_relationship(parent, child):
    return child in parent.home.children.all()


def is_subjectroom_student_relationship(subjectroom, student):
    return student in subjectroom.students.all()


def is_classroom_student_relationship(classroom, student):
    return student in classroom.students.all()

def is_assignment_teacher_relationship(assignment, teacher):
    return is_subjectroom_classteacher_relationship(assignment.get_subjectroom(), teacher) or (
        (assignment.get_subjectroom()).teacher == teacher)


def is_student_corrected_assignment_relationship(student, assignment):
    """
    Checks if the given student has been assigned the given assignment and if the given assignment is corrected
    """
    return (is_student_assignment_relationship(student, assignment) and is_assignment_corrected(assignment))


def is_open_student_corrected_assignment_relationship(student, assignment):
    return (is_corrected_open_assignment(assignment)) and (
    student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT) and (assignment.content_object == student)

def is_student_assignment_relationship(student, assignment):
    """
    Checks if the given student has been assigned the given assignment (via subjectroom, remedial, or practice)
    """
    return student in assignment.content_object.students.all()

def is_hwcentral_team_admin(user):
    """
    Checks if the given user is a super-admin set up for use by the hwcentral team
    """
    from core.utils.references import HWCentralGroup
    return (user.userinfo.group == HWCentralGroup.refs.ADMIN) and (user.username.startswith('hwcadmin_school_'))