# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0016_user_last_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.NullBooleanField(default=None, verbose_name='\u041f\u043e\u043b'),
        ),
    ]
