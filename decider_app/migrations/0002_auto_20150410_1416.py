# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'd_social_site',
                'verbose_name': '\u0421\u043e\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0430\u0439\u0442',
                'verbose_name_plural': '\u0421\u043e\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u0441\u0430\u0439\u0442\u044b',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='social_id',
            field=models.CharField(max_length=100, null=True, verbose_name='social site id', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='social_site',
            field=models.ForeignKey(blank=True, to='decider_app.SocialSite', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('social_site', 'social_id')]),
        ),

    ]
