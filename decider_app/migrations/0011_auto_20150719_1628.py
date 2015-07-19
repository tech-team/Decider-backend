# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0010_auto_20150718_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.NullBooleanField(default=False, verbose_name='\u041f\u043e\u043b'),
        ),
    ]
