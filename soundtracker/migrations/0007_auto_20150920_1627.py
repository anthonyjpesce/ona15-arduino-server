# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0006_auto_20150920_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='arduino_number',
        ),
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 23, 27, 3, 880872, tzinfo=utc)),
        ),
    ]
