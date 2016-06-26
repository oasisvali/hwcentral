from django.db.models import Q

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
            from core.models import Group
            self.STUDENT = Group.objects.get(name='student')
            self.TEACHER = Group.objects.get(name='teacher')
            self.PARENT = Group.objects.get(name='parent')
            self.ADMIN = Group.objects.get(name='admin')
            self.OPEN_STUDENT = Group.objects.get(name='open_student')


class HWCentralOpen(LazyReference):
    @classmethod
    def build_refs(cls):
        return HWCentralOpen.HWCentralOpenRefs()

    class HWCentralOpenRefs(object):
        def __init__(self):
            from core.models import School, SubjectRoom, ClassRoom
            self.SCHOOL = School.objects.get(pk=2)
            self.CLASSROOM = ClassRoom.objects.get(school=self.SCHOOL, standard__number=0)
            self.SUBJECTROOMS = SubjectRoom.objects.filter(classRoom=self.CLASSROOM)

class EdgeSpecialTags(LazyReference):
    @classmethod
    def build_refs(cls):
        return EdgeSpecialTags.EdgeSpecialTagsRefs()

    class EdgeSpecialTagsRefs(object):
        def __init__(self):
            from core.models import QuestionTag
            self.APPLICATION = QuestionTag.objects.get(name='application')
            self.CONCEPTUAL = QuestionTag.objects.get(name='conceptual')
            self.CRITICAL_THINKING = QuestionTag.objects.get(name='critical thinking')

            self.FILTER = Q(questiontag=self.APPLICATION) | Q(questiontag=self.CONCEPTUAL) | Q(
                questiontag=self.CRITICAL_THINKING)
            self.PKS = [
                self.APPLICATION.pk,
                self.CONCEPTUAL.pk,
                self.CRITICAL_THINKING.pk
            ]

class HWCentralRepo(LazyReference):
    @classmethod
    def build_refs(cls):
        return HWCentralRepo.HWCentralRepoRefs()

    class HWCentralRepoRefs(object):
        def __init__(self):
            from core.models import School
            self.SCHOOL = School.objects.get(pk=1)