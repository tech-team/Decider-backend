from decider_api.log_manager import logger
from decider_api.utils.gcm_helper import send_push
from push_service.app import app
from push_service.utils.notification_codes import CODE_NEW_VOTE
from push_service.utils.notification_helper import send_notification


@app.task()
def vote_notification(user_id, question_id):
    send_notification(CODE_NEW_VOTE, 'vote', 'question', question_id, user_id, question_id=question_id)


@app.task()
def many_votes_notification(user_id, question_id, votes_num):
    send_notification(CODE_NEW_VOTE, 'vote_many', 'question', question_id, user_id, question_id=question_id,
                                                                                    count=votes_num)
