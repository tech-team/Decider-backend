# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=100, verbose_name='email address')),
                ('username', models.CharField(default=b'', max_length=50, verbose_name='username', blank=True)),
                ('first_name', models.CharField(default=b'', max_length=50, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(default=b'', max_length=50, verbose_name='last name', blank=True)),
                ('middle_name', models.CharField(default=b'', max_length=50, verbose_name='middle_name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateField(null=True, verbose_name='\u0414\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('city', models.CharField(max_length=50, verbose_name='\u0413\u043e\u0440\u043e\u0434', blank=True)),
                ('about', models.TextField(max_length=1000, verbose_name='\u041e \u0441\u0435\u0431\u0435', blank=True)),
                ('gender', models.BooleanField(default=False, verbose_name='\u041f\u043e\u043b')),
                ('avatar_url', models.CharField(default=b'', max_length=255, verbose_name='avatar url', blank=True)),
            ],
            options={
                'ordering': ('-date_joined',),
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', max_length=1000, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u044f', blank=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
                'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(to='decider_app.Comment')),
            ],
            options={
                'db_table': 'comment_likes',
                'verbose_name': '\u041b\u0430\u0439\u043a \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u044f',
                'verbose_name_plural': '\u041b\u0430\u0439\u043a\u0438 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0435\u0432',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'country',
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('items_count', models.SmallIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u043e\u0432')),
            ],
            options={
                'db_table': 'poll',
                'verbose_name': '\u0413\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u043a\u0430',
                'verbose_name_plural': '\u0413\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='PollItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(default=b'', max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u0430', blank=True)),
                ('image_url', models.CharField(default=b'', max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0443', blank=True)),
                ('votes_count', models.SmallIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043e\u043b\u043e\u0441\u043e\u0432')),
                ('poll', models.ForeignKey(to='decider_app.Poll')),
            ],
            options={
                'db_table': 'poll_item',
                'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u043a\u0438',
                'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b\u043e\u043a',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', max_length=500, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0432\u043e\u043f\u0440\u043e\u0441\u0430', blank=True)),
                ('is_closed', models.BooleanField(default=False, verbose_name='\u0417\u0430\u043a\u0440\u044b\u0442?')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='liked_questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
                'db_table': 'question',
                'verbose_name': '\u0412\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poll', models.ForeignKey(to='decider_app.Poll')),
                ('poll_item', models.ForeignKey(to='decider_app.PollItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'vote',
                'verbose_name': '\u0413\u043e\u043b\u043e\u0441',
                'verbose_name_plural': '\u0413\u043e\u043b\u043e\u0441\u0430',
            },
        ),
        migrations.AddField(
            model_name='pollitem',
            name='question',
            field=models.ForeignKey(to='decider_app.Question'),
        ),
        migrations.AddField(
            model_name='pollitem',
            name='votes',
            field=models.ManyToManyField(related_name='voted_poll_items', through='decider_app.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='question',
            field=models.ForeignKey(to='decider_app.Question'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='question',
            field=models.ForeignKey(to='decider_app.Question'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='liked_comments', through='decider_app.CommentLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='decider_app.Country', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
