# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0018_auto_20150723_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='spam_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='spam_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
