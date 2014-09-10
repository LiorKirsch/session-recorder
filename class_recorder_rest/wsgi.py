import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'class_recorder_rest.settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
