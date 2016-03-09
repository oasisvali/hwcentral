from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from core.utils.constants import HWCentralEnv
from hwcentral.settings import ENVIRON, CONTACT_PHONE, CONTACT_EMAIL, SALES_PHONE


def settings(request):
    """
    Context Processor that provides access to the current settings for all templates
    """
    return {
        'ENABLE_ANALYTICS': (ENVIRON == HWCentralEnv.PROD),
        'CONTACT_PHONE': CONTACT_PHONE,
        'SALES_PHONE': SALES_PHONE,
        'CONTACT_EMAIL': CONTACT_EMAIL,
        'OVERVIEW_VIDEO': "http://%s%s" % (Site.objects.get_current().domain, reverse('overview_video'))
    }
