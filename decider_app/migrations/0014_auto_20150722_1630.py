# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0013_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='share_image',
            field=models.ForeignKey(blank=True, to='decider_app.Picture', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='decider_app.Category', null=True),
        ),
    ]
