# Place stuff in here that only needs to run once on startup

# HWCentral should be config driven, load all the HWCentral-specific config files
from hwcentral.hwcentral_config import load_site_configs

load_site_configs()
