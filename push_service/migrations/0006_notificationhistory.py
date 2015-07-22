# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_service', '0005_gcmclient_subscribed'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(max_length=255, choices=[(b'comment', b'comment'), (b'question_like', b'question_like'), (b'comment_like', b'comment_like'), (b'poll', b'poll')])),
                ('entity_id', models.IntegerField()),
                ('action', models.CharField(max_length=255, choices=[(b'new', b'new')])),
                ('client', models.ForeignKey(to='push_service.GcmClient')),
            ],
            options={
                'db_table': 'd_notification_history',
                'verbose_name': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043e\u043a',
            },
        ),
    ]
