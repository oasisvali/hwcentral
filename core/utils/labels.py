# NOTE: It is fine if this is duplicating some of the models' unicode methods.
# keep database labels in models.py and frontend labels here
# E.G. database label for classroom would include school name, but for frontend, it shouldnt

def get_classroom_label(classroom):
    return '{0} - {1}'.format(classroom.standard.number, classroom.division)


def get_user_label(user):
    return '{0} {1}'.format(user.first_name, user.last_name)


def get_date_label(date):
    return date.strftime('%b %d')


def get_fraction_label(fraction):
    return int(round(fraction * 100, 0))


def get_subjectroom_label(subjectroom):
    return '{0} - {1} {2}'.format(subjectroom.classRoom.standard.number, subjectroom.classRoom.division,
                                  subjectroom.subject.name)