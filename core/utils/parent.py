from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.utils.base import UserUtils
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils


class ParentUtils(UserUtils):
    def __init__(self, parent):
        self.UTILS_GROUP = HWCentralGroup.refs.PARENT
        super(ParentUtils, self).__init__(parent)

    def get_announcements_query(self):
        announcements_query = Q()
        for child in self.user.home.children.all():
            child_utils = StudentUtils(child)
            announcements_query = announcements_query | child_utils.get_announcements_query()
        return announcements_query | Q(content_type=ContentType.objects.get_for_model(User), object_id=self.user.pk)
