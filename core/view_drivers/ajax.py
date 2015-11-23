from core.utils.admin import AdminUtils
from core.utils.json import HWCentralJsonResponse
from core.utils.parent import ParentUtils
from core.utils.student import StudentUtils
from core.utils.teacher import TeacherUtils
from core.view_drivers.base import GroupDriven
from core.view_models.ajax import AnnouncementRow


class GroupDrivenAjax(GroupDriven):
    """
    Abstract class that provides common functionality required by all ajax data endpoints which have different logic
    for different user group
    """
    pass

class AnnouncementsAjaxGet(GroupDrivenAjax):
    @classmethod
    def formatted_response(cls, utils):
        return HWCentralJsonResponse([AnnouncementRow(announcement) for announcement in utils.get_announcements()])

    def student_endpoint(self):
        return AnnouncementsAjaxGet.formatted_response(StudentUtils(self.user))

    def teacher_endpoint(self):
        return AnnouncementsAjaxGet.formatted_response(TeacherUtils(self.user))

    def admin_endpoint(self):
        return AnnouncementsAjaxGet.formatted_response(AdminUtils(self.user))

    def parent_endpoint(self):
        return AnnouncementsAjaxGet.formatted_response(ParentUtils(self.user))

