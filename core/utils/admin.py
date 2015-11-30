import django
from django.db.models import Avg

from core.models import ClassRoom, SubjectRoom, Assignment
from core.utils.references import HWCentralGroup
from core.utils.teacher import TeacherAdminSharedUtils, TeacherAdminSharedSubjectIdUtils


class AdminGroupUtils(object):
    """
    mixin to enable admin user group checking
    """

    def __init__(self):
        self.UTILS_GROUP = HWCentralGroup.refs.ADMIN

class AdminUtils(AdminGroupUtils, TeacherAdminSharedUtils):
    def __init__(self, admin):
        AdminGroupUtils.__init__(self)
        TeacherAdminSharedUtils.__init__(self, admin)

    def get_managed_subjectroom_ids(self):
        return SubjectRoom.objects.filter(classRoom__school=self.user.userinfo.school).values_list('pk', flat=True)

    def get_managed_classrooms(self):
        return ClassRoom.objects.filter(school=self.user.userinfo.school)

    def get_managed_classroom_ids(self):
        return self.get_managed_classrooms().values_list('pk', flat=True)

    def get_classrooms_table_classroom_rows(self):
        from core.view_models.home import ClassroomsTableClassroomRow, ClassroomsTableSubjectroomRow
        results = []
        now = django.utils.timezone.now()
        for classroom in self.get_managed_classrooms():
            subjectroom_rows = []
            for subjectroom in SubjectRoom.objects.filter(classRoom=classroom):
                subjectroom_rows.append(ClassroomsTableSubjectroomRow(subjectroom,
                                                                    Assignment.objects.filter(subjectRoom=subjectroom,
                                                                                              due__lte=now).aggregate(
                                                                        Avg("average"))['average__avg']))
            results.append(ClassroomsTableClassroomRow(classroom, subjectroom_rows))

        return results

class AdminSubjectIdUtils(AdminGroupUtils, TeacherAdminSharedSubjectIdUtils):
    def __init__(self, admin, subjectroom):
        AdminGroupUtils.__init__(self)
        TeacherAdminSharedSubjectIdUtils.__init__(self, admin, subjectroom)
