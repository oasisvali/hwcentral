def get_classroom_label(classroom):
    return '{0} - {1}'.format(classroom.standard.number, classroom.division)


def get_user_label(user):
    return '{0} {1}'.format(user.first_name, user.last_name)