from core.models import ClassRoom, SubjectRoom
from core.utils.references import HWCentralGroup
from core.utils.teacher import TeacherAdminSharedUtils


class AdminUtils(TeacherAdminSharedUtils):
    def __init__(self, admin):
        assert admin.userinfo.group == HWCentralGroup.refs.ADMIN
        super(AdminUtils, self).__init__(admin)

    def get_managed_subjectroom_ids(self):
        return SubjectRoom.objects.filter(classRoom__school=self.user.userinfo.school).values_list('pk', flat=True)

    def get_managed_classroom_ids(self):
        return ClassRoom.objects.filter(school=self.user.userinfo.school).values_list('pk', flat=True)
