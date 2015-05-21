# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decider_app', '0002_auto_20150410_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'd_locale',
                'verbose_name': '\u041b\u043e\u043a\u0430\u043b\u044c',
                'verbose_name_plural': '\u041b\u043e\u043a\u0430\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='LocaleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'db_table': 'd_locale_category',
                'verbose_name': '\u041b\u043e\u043a\u0430\u043b\u044c \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438',
                'verbose_name_plural': '\u041b\u043e\u043a\u0430\u043b\u0438 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0439',
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AddField(
            model_name='localecategory',
            name='category',
            field=models.ForeignKey(to='decider_app.Category'),
        ),
        migrations.AddField(
            model_name='localecategory',
            name='locale',
            field=models.ForeignKey(to='decider_app.Locale'),
        ),
        migrations.AddField(
            model_name='locale',
            name='categories',
            field=models.ManyToManyField(related_name='locales', through='decider_app.LocaleCategory', to='decider_app.Category'),
        ),
    ]
