# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entries',
            old_name='Progress',
            new_name='progress',
        ),
        migrations.AddField(
            model_name='entries',
            name='name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
