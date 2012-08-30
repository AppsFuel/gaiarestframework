from django.conf import settings

GAIA_TITLE = getattr(settings, "GAIA_TITLE", 'GAIA')
GAIA_VERSION = getattr(settings, "GAIA_VERSION", 'beta')
