# coding=utf-8
from decider_api.log_manager import logger
from decider_api.utils.gcm_helper import send_push
from push_service.app import app

__author__ = 'snake'


@app.task()
def comment_notification(user_id, question_id, comment_id):
    from push_service.models import GcmClient
    print(user_id)
    receivers = GcmClient.objects.filter(user_id=user_id)
    notification = {
        'title': "Decider",
        'msg': u"У вас новый комментарий!"
    }
    data = {
        'question_id': question_id,
        'comment_id': comment_id
    }
    for receiver in receivers:
        logger.error(send_push(receiver.registration_token, notification, data))
