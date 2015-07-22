from decider_api.log_manager import logger
from decider_api.utils.gcm_helper import send_push
from push_service.app import app
from push_service.utils.notification_codes import CODE_NEW_VOTE


@app.task()
def vote_notification(user_id, question_id):
    from push_service.models import NotificationHistory, GcmClient

    receivers = GcmClient.objects.filter(user_id=user_id)
    data = {
        'code': CODE_NEW_VOTE,
        'question_id': question_id
    }
    for receiver in receivers:
        if NotificationHistory.objects.filter(client=receiver, entity='question', action='vote').count() == 0:
            NotificationHistory.objects.create(client=receiver, entity='question', action='vote', entity_id=question_id,
                                               user_id=user_id)
            resp = send_push(receiver.registration_token, data)
            logger.error(resp)
