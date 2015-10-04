from django.http import HttpResponse


class HWCentralFileResponse(HttpResponse):
    def __init__(self, filename, bytestring, *args, **kwargs):
        super(HWCentralFileResponse, self).__init__(bytestring, content_type='application/octet-stream', *args,
                                                    **kwargs)
        self['Content-Disposition'] = 'attachment; filename=\"%s\"' % filename
