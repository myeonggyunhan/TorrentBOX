# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20150806_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='TorrentGlobalEntries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('hash_value', models.CharField(max_length=40)),
                ('progress', models.PositiveSmallIntegerField(default=0, null=True)),
                ('file_size', models.BigIntegerField(default=0, null=True)),
                ('downloaded_size', models.BigIntegerField(default=0, null=True)),
                ('peers', models.PositiveSmallIntegerField(default=0, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
