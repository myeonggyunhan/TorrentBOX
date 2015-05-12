# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_value', models.CharField(max_length=40)),
                ('Progress', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
