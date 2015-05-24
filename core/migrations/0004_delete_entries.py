# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150323_0110'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Entries',
        ),
    ]
