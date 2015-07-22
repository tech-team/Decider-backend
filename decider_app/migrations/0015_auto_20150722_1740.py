# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0014_auto_20150722_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentlike',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        # migrations.AddField(
        #     model_name='user',
        #     name='last_active',
        #     field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c'),
        # ),
        migrations.AddField(
            model_name='vote',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
    ]
