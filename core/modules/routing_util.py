from django.conf.urls import url


class UrlName():
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^' + self.name + '/$'
        self.template = self.name + '.html'

    def create_static_route(self, regex_override=None):

        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from routers import static_router

        if regex_override is not None:
            url_matcher = regex_override
        else:
            url_matcher = self.url_matcher
        return url(url_matcher, static_router, {'template': self.template}, name=self.name)


class UrlNames():
    INDEX = UrlName('index')
    HOME = UrlName('home')

    SITE_ANCHOR = UrlName('site_anchor')

    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = UrlName('login')

    NEWS = UrlName('news')
    CONTACT = UrlName('contact')
    ABOUT = UrlName('about')