from django import template
from gaiarestframework.settings import *

register = template.Library()


@register.simple_tag
def gaia_title():
    return GAIA_TITLE


@register.simple_tag
def gaia_version():
    return GAIA_VERSION
