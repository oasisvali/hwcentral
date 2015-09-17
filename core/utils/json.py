from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from hwcentral import settings


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

class Json404Response(JsonResponse, HttpResponseNotFound):
    message = "Resource Not Found"

    def __init__(self, message=None):
        if message is not None and settings.DEBUG:
            self.message = message
        super(Json404Response, self).__init__({"message": self.message})

def get_object_or_Json404(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404, e:
        return str(e)
