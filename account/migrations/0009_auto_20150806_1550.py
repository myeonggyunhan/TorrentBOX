# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_torrententries_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrententries',
            name='progress',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
    ]
