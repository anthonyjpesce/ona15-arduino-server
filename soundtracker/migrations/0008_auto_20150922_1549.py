# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0007_auto_20150920_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='robot',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='signal',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
