# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_service', '0008_notificationhistory_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationhistory',
            name='type',
            field=models.CharField(default=b'push', max_length=255, choices=[(b'email', b'email'), (b'push', b'push')]),
        ),
        migrations.AlterField(
            model_name='notificationhistory',
            name='action',
            field=models.CharField(max_length=255, choices=[(b'new', b'new'), (b'new_many', b'new_many')]),
        ),
    ]
