# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150524_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrententries',
            name='downloaded_size',
            field=models.BigIntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='torrententries',
            name='file_size',
            field=models.BigIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
