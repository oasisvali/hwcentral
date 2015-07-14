from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from core.view_models.json import JSONViewModel


class HWCentralJsonResponse(JsonResponse):
    def __init__(self, response_object):
        super(HWCentralJsonResponse, self).__init__(response_object, encoder=HWCentralJSONEncoder, safe=False)


class HWCentralJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, JSONViewModel):
            return o.get_json()
        return super(HWCentralJSONEncoder, self).default(o)