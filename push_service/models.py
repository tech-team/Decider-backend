# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class GcmClient(models.Model):
    class Meta:
        verbose_name = _(u'Клиент рассылки')
        verbose_name_plural = _(u'Клиенты рассылок')
        db_table = "d_gcm_client"

    instance_id = models.CharField(max_length=255)
    registration_token = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.instance_id
