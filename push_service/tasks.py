from __future__ import absolute_import
from datetime import timedelta
from django.db.models.loading import get_model
from django.utils import timezone

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decider_backend.settings')

app = Celery('push')
app.config_from_object('push_service.celery_config')


if __name__ == '__main__':
    app.start()


@app.task()
def test_periodic():
    print(get_model('decider_app', 'question').objects.filter(creation_date__gt=timezone.now()-timedelta(hours=1)).count())
