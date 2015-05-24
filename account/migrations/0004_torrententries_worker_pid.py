# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_torrententries_download_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrententries',
            name='worker_pid',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
