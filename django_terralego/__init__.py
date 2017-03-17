import os

from .conf import TERRALEGO

if 'URL' in TERRALEGO:
    os.environ['TERRALEGO_URL'] = TERRALEGO['URL']
if 'USER' in TERRALEGO:
    os.environ['TERRALEGO_USER'] = TERRALEGO['USER']
if 'PASSWORD' in TERRALEGO:
    os.environ['TERRALEGO_PASSWORD'] = TERRALEGO['PASSWORD']
