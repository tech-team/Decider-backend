# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_service', '0004_auto_20150719_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='gcmclient',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
