# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150524_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrententries',
            name='peers',
            field=models.PositiveSmallIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
