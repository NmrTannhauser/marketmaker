import os
import django
import sys

path = os.path.expanduser('/home/projects/')
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mmsite.settings'

django.setup()

from views import getPrivateKey


def getPK():
    return getPrivateKey()
