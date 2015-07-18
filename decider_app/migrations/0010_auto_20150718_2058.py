# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0009_auto_20150522_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(unique=True, max_length=50, verbose_name='unique id for user', db_index=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=b'', max_length=50, verbose_name='username', db_index=True, blank=True),
        ),
    ]
