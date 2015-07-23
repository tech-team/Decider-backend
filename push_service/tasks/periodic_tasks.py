from datetime import timedelta
from django.utils import timezone
from decider_app.models import Vote
from push_service.app import app
from push_service.tasks.comment_notification import many_comments_notification
from push_service.tasks.vote_notification import many_votes_notification

RECENT_TIMEDELTA = 60   # minutes
PERIODIC_TIMEDELTA = 6  # hours
CHANGES_TIMEDELTA = 24  # hours
COUNT_THRESHOLD = 10

@app.task()
def send_many_comments_notifications():
    from decider_app.models import Question
    from push_service.models import NotificationHistory
    questions = Question.objects.prefetch_related('comment_set', 'author')\
                                .filter(creation_date__lte=timezone.now() - timedelta(hours=PERIODIC_TIMEDELTA))

    for question in questions:
        count = question.comment_set.filter(creation_date__gte=timezone.now() - timedelta(hours=CHANGES_TIMEDELTA)).count()
        recent_history = NotificationHistory.objects.filter(user_id=question.author_id,
                                                            date_created__gt=timezone.now() - timedelta(minutes=RECENT_TIMEDELTA))

        if count >= COUNT_THRESHOLD \
                and not NotificationHistory.objects.filter(user_id=question.author_id, entity='comment', action='new_many'):
            if recent_history:
                many_comments_notification.apply_async((question.author_id, question.id, count),
                                                       eta=timezone.now() + timedelta(minutes=RECENT_TIMEDELTA))
            else:
                many_comments_notification.apply_async((question.author_id, question.id, count),)

@app.task()
def send_many_votes_notifications():
    from decider_app.models import Question
    from push_service.models import NotificationHistory
    questions = Question.objects.filter(creation_date__lte=timezone.now() - timedelta(hours=PERIODIC_TIMEDELTA))

    for question in questions:
        count = Vote.objects.filter(creation_date__gte=timezone.now() - timedelta(hours=CHANGES_TIMEDELTA),
                                    poll_item__question=question).count()
        recent_history = NotificationHistory.objects.filter(user_id=question.author_id,
                                                            date_created__gt=timezone.now() - timedelta(minutes=RECENT_TIMEDELTA))

        if count >= COUNT_THRESHOLD \
                and not NotificationHistory.objects.filter(user_id=question.author_id, entity='question', action='vote_many'):
            if recent_history:
                many_votes_notification.apply_async((question.author_id, question.id, count),
                                                       eta=timezone.now() + timedelta(minutes=RECENT_TIMEDELTA))
            else:
                many_votes_notification.apply_async((question.author_id, question.id, count),)


@app.task()
def send_periodic_notifications():
    send_many_comments_notifications.apply_async()
    send_many_votes_notifications.apply_async()
