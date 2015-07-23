# coding=utf-8
from push_service.app import app
from push_service.utils.notification_codes import CODE_NEW_COMMENT, CODE_NEW_COMMENT_LIKE, CODE_MANY_COMMENTS
from push_service.utils.notification_helper import send_notification


@app.task()
def comment_notification(user_id, question_id, comment_id):
    send_notification(CODE_NEW_COMMENT, 'new', 'comment', comment_id, user_id, question_id=question_id)


@app.task()
def comment_like_notification(user_id, question_id, comment_id):
    send_notification(CODE_NEW_COMMENT_LIKE, 'like', 'comment', comment_id, user_id, question_id=question_id,
                                                                                     comment_id=comment_id)


@app.task()
def many_comments_notification(user_id, question_id, comments_num):
    send_notification(CODE_MANY_COMMENTS, 'new_many', 'comment', None, user_id, question_id=question_id,
                                                                                count=comments_num)
