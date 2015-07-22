from __future__ import absolute_import

import os
from celery import Celery
from decider_backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decider_backend.settings')

app = Celery('push')
app.config_from_object('push_service.celery_config')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()

