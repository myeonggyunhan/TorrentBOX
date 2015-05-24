# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_torrententries_worker_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrententries',
            name='worker_pid',
            field=models.PositiveIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
