# coding=utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from decider_app.models import User


class GcmClient(models.Model):
    class Meta:
        verbose_name = _(u'Клиент рассылки')
        verbose_name_plural = _(u'Клиенты рассылок')
        db_table = "d_gcm_client"

    instance_id = models.CharField(max_length=255)
    registration_token = models.CharField(max_length=255, null=True, blank=True)
    subscribed = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, db_index=True)

    def __unicode__(self):
        return self.instance_id


class NotificationHistory(models.Model):
    class Meta:
        verbose_name = _(u'История рассылок')
        db_table = "d_notification_history"

    ENTITIES = (('comment', 'comment'),
                ('question_like', 'question_like'),
                ('comment_like', 'comment_like'),
                ('poll', 'poll'))
    ACTIONS = (('new', 'new'),
               ('new_many', 'new_many'),
               ('like', 'like'),
               ('like_many', 'like_many'),
               ('inactive', 'inactive'),
               ('vote', 'vote'),
               ('vote_many', 'vote_many'))
    TYPES = (('email', 'email'),
             ('push', 'push'))

    client = models.ForeignKey(GcmClient)
    user = models.ForeignKey(User, null=True, blank=True)
    entity = models.CharField(max_length=255, choices=ENTITIES)
    entity_id = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=255, choices=ACTIONS)
    date_created = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=255, choices=TYPES, default='push')
