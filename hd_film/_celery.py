from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hd_film.settings')

app = Celery('hd_film')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()