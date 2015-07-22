# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_service', '0009_auto_20150722_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationhistory',
            name='action',
            field=models.CharField(max_length=255, choices=[(b'new', b'new'), (b'new_many', b'new_many'), (b'like', b'like'), (b'like_many', b'like_many'), (b'inactive', b'inactive')]),
        ),
    ]
