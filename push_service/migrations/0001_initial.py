# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GcmClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_id', models.CharField(max_length=255)),
                ('registration_token', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'd_gcm_client',
                'verbose_name': '\u041a\u043b\u0438\u0435\u043d\u0442 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
                'verbose_name_plural': '\u041a\u043b\u0438\u0435\u043d\u0442\u044b \u0440\u0430\u0441\u0441\u044b\u043b\u043e\u043a',
            },
        ),
    ]
