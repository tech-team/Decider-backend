from datetime import timedelta
from decider_backend.settings import RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST

BROKER_URL = 'amqp://' + RABBITMQ_USER + \
             ':'       + RABBITMQ_PASS + \
             '@'       + RABBITMQ_HOST + \
             ':'       + RABBITMQ_PORT + \
             '/'      + RABBITMQ_VHOST


CELERYD_CONCURRENCY = 8

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_TIME_LIMIT = 20
CELERY_TASK_SOFT_TIME_LIMIT = 10

CELERY_IMPORTS = ('decider_api.views.question_views', 'push_service.tasks.comment_notification',
                  'push_service.tasks.vote_notification', 'push_service.tasks.periodic_tasks')
# CELERY_TIMEZONE = 'Europe/Moscow'

CELERYBEAT_SCHEDULE = {
    'many': {
        'task': 'push_service.tasks.periodic_tasks.send_periodic_notifications',
        'schedule': timedelta(hours=6)
    }
}
