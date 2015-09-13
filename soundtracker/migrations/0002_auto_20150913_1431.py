# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soundtracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signal',
            options={'ordering': ('-timestamp', 'pk')},
        ),
    ]
