import re

from django.http import HttpResponse


def merge_dicts(dict_list):
    """
    dict with higher index overwrites dict with lower index in case of matching key
    """
    merged_dict = {}
    for dictionary in dict_list:
        merged_dict.update(dictionary)
    return merged_dict

def make_string_lean(string):
    """
    collapses all whitespace in string and strips whitespace from ends
    """

    whitespace = re.compile(r'\s+')
    string = whitespace.sub(' ', string)
    return string.strip()


class HWCentralFileResponse(HttpResponse):
    """
    Use this to download data as a file served by the backend
    """

    def __init__(self, filename, bytestring, *args, **kwargs):
        super(HWCentralFileResponse, self).__init__(bytestring, content_type='application/octet-stream', *args,
                                                    **kwargs)
        self['Content-Disposition'] = 'attachment; filename=\"%s\"' % filename
