from django.conf import settings


try:
    TERRALEGO = settings.TERRALEGO
except AttributeError:
    TERRALEGO = {}
