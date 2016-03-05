from core.utils.constants import HWCentralEnv
from hwcentral.settings import ENVIRON


def settings(request):
    """
    Context Processor that provides access to the current settings for all templates
    """
    return {
        'ENABLE_ANALYTICS': (ENVIRON == HWCentralEnv.PROD)
    }
