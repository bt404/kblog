import os
import django.core.handlers.wsgi

import sae

os.environ['DJANGO_SETTINGS_MODULE'] = 'kblog.settings'

application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler())
