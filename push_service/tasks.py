from celery import Celery
from push_service.celery_config import broker

app = Celery('push', broker=broker)