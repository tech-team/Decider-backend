# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0019_auto_20150723_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(max_length=255, choices=[(b'question', b'question'), (b'comment', b'comment')])),
                ('entity_id', models.PositiveIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_spam_report',
                'verbose_name': '\u041f\u043e\u043c\u0435\u0442\u043a\u0430 \u043e \u0441\u043f\u0430\u043c\u0435',
                'verbose_name_plural': '\u041f\u043e\u043c\u0435\u0442\u043a\u0438 \u043e \u0441\u043f\u0430\u043c\u0435',
            },
        ),
    ]
