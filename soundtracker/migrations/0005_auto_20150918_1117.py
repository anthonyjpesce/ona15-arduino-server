# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0004_auto_20150918_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, null=True, blank=True)),
                ('location', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 18, 17, 48, 891807, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='signal',
            name='robot',
            field=models.ForeignKey(to='soundtracker.Robot', null=True),
        ),
    ]
