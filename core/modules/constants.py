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

# TODO: This is data-redundancy wrt database. Fix it by reading the string values from the db
class HWCentralGroup(object):
    ADMIN = 'Admin'
    PARENT = 'Parent'
    STUDENT = 'Student'
    TEACHER = 'Teacher'

