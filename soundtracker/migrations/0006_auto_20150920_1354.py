# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0005_auto_20150918_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='name',
            field=models.CharField(default=b'Unnamed robot', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 54, 3, 980673, tzinfo=utc)),
        ),
    ]
