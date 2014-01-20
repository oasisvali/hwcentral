from django.conf.urls import url


class UrlName():
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^' + self.name + '/$'
        self.template = self.name + '.html'

    def create_static_route(self):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.template}, name=self.name)


class UrlNames():
    INDEX = UrlName('index')
    HOME = UrlName('home')

    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = UrlName('login')

    NEWS = UrlName('news')
    CONTACT = UrlName('contact')
    ABOUT = UrlName('about')