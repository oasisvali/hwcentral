import json

from django.utils.safestring import mark_safe

from core.models import QuestionTag
from core.utils.references import EdgeSpecialTags
from core.view_models.base import VM


class Tags(VM):
    def __init__(self):
        tags_list = [{"name": t.name} for t in
                     QuestionTag.objects.exclude(pk__in=EdgeSpecialTags.refs.PKS).order_by('name')]

        self.tags_list_json = mark_safe(json.dumps(tags_list))
