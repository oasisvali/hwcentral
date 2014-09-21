VIEWMODEL_KEY = 'vm'


class HWCentralRegex(object):
    USERNAME = r'[\w.@+-]+'
    GENERAL = r'[\w-]+'
    NUMERIC = r'\d+'


class HttpMethod(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class HWCentralGroup(object):
    STUDENT = 1
    TEACHER = 2
    PARENT = 3
    ADMIN = 4

