import os

from django.conf import settings


terralego_settings = settings.get('TERRALEGO', {})

if 'URL' in terralego_settings:
    os.environ['TERRALEGO_URL'] = terralego_settings['URL']
if 'USER' in terralego_settings:
    os.environ['TERRALEGO_USER'] = terralego_settings['USER']
if 'PASSWORD' in terralego_settings:
    os.environ['TERRALEGO_PASSWORD'] = terralego_settings['PASSWORD']
