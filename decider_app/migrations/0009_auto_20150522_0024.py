# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0008_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='question',
            field=models.OneToOneField(to='decider_app.Question'),
        ),
    ]
