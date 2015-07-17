from core.models import Group


class HWCentralGroup(object):
    STUDENT = Group.objects.get(name='student')
    TEACHER = Group.objects.get(name='teacher')
    PARENT = Group.objects.get(name='parent')
    ADMIN = Group.objects.get(name='admin')