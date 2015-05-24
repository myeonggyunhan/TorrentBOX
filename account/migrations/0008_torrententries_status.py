# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_torrententries_peers'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrententries',
            name='status',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
