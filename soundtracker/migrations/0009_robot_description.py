# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0008_auto_20150922_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
