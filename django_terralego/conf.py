from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    TERRALEGO = settings.TERRALEGO
except AttributeError:
    TERRALEGO = {}
