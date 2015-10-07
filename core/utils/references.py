from core.models import Group, School


# All db-driven references should follow this lazy-loading pattern to prevent ./manage.py from shitting itself when running
# off a flushed database

class LazyMetaClass(type):
    @property
    def refs(cls):
        if getattr(cls, '_REFS', None) is None:
            refs = cls.build_refs()
            cls._REFS = refs
        return cls._REFS


class LazyReference(object):
    __metaclass__ = LazyMetaClass

    @classmethod
    def build_refs(cls):
        raise NotImplementedError("Subclass of LazyReference must implement build_refs")


class HWCentralGroup(LazyReference):
    @classmethod
    def build_refs(cls):
        return HWCentralGroup.HWCentralGroupRefs()

    class HWCentralGroupRefs(object):
        def __init__(self):
            self.STUDENT = Group.objects.get(name='student')
            self.TEACHER = Group.objects.get(name='teacher')
            self.PARENT = Group.objects.get(name='parent')
            self.ADMIN = Group.objects.get(name='admin')

class HWCentralRepo(LazyReference):
    @classmethod
    def build_refs(cls):
        return HWCentralRepo.HWCentralRepoRefs()

    class HWCentralRepoRefs(object):
        def __init__(self):
            self.SCHOOL = School.objects.get(pk=1)