# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0006_auto_20150426_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='preview_url',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u043f\u0440\u0435\u0432\u044c\u044e', blank=True),
        ),
    ]
