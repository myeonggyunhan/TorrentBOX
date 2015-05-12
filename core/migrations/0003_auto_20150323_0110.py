# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150323_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='progress',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
    ]
