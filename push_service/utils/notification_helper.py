from decider_api.log_manager import logger
from decider_api.utils.gcm_helper import send_push


def send_notification(code, action, entity, entity_id, user_id, **kwargs):
    from push_service.models import NotificationHistory, GcmClient

    receivers = GcmClient.objects.filter(user_id=user_id)
    data = {
        'code': code,
    }
    data.update(kwargs)
    for receiver in receivers:
        if NotificationHistory.objects.filter(client=receiver, entity=entity, action=action).count() == 0:
            NotificationHistory.objects.create(client=receiver, entity=entity, action=action, entity_id=entity_id,
                                               user_id=user_id)
            resp = send_push(receiver.registration_token, data)
            logger.error(resp)
