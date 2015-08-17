from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class HWCentralJsonResponse(JsonResponse):
    def __init__(self, response_object):
        super(HWCentralJsonResponse, self).__init__(response_object, encoder=HWCentralJSONEncoder, safe=False)


class HWCentralJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, JSONModel):
            return o.get_json()
        return super(HWCentralJSONEncoder, self).default(o)


class JSONModel(object):
    def get_json(self):
        return self.__dict__