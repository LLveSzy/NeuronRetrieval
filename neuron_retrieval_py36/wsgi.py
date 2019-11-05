"""
WSGI config for neuron_display project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append("/var/neuron_retrieval/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neuron_retrieval_py36.settings")

application = get_wsgi_application()
