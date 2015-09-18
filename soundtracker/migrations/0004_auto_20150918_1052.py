# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0003_auto_20150916_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 17, 52, 38, 128485, tzinfo=utc)),
        ),
    ]
