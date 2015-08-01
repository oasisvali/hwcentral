from hwcentral import settings


def current_domain(request):
        if settings.DEBUG:
            current_domain = '127.0.0.1:8000'
        else:
            current_domain ='hwcentral.in'

        return {
            'current_domain':current_domain,
        }
