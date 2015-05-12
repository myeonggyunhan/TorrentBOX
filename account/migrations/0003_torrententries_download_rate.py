# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150501_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrententries',
            name='download_rate',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
    ]
