from core.modules.helpers import UrlName

VIEWMODEL_KEY = 'vm'

class HttpMethod():
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class UrlNames():
    LOGIN = UrlName('login')
    INDEX = UrlName('index')
    HOME = UrlName('home')
    NEWS = UrlName('news')
    CONTACT = UrlName('contact')
    ABOUT = UrlName('about')
    SITE_ANCHOR = UrlName('site_anchor')
    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')

