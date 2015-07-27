# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0020_spamreport'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0430', 'select_on_save': True, 'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u044b'},
        ),
    ]
