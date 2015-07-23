# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_auto_20150630_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='home',
            old_name='students',
            new_name='children',
        ),
    ]
