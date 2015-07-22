# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('push_service', '0007_notificationhistory_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationhistory',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
