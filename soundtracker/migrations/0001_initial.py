# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arduino_number', models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('voltage', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
        ),
    ]
