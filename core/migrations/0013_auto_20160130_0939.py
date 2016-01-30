# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_auto_20160130_0936'),
    ]

    operations = [
        migrations.RemoveField(
                model_name='assignment',
                name='content_type',
        ),
        migrations.RemoveField(
                model_name='assignment',
                name='object_id',
        ),
    ]
