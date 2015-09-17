# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0002_auto_20150913_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 4, 24, 36, 941586, tzinfo=utc)),
        ),
    ]
