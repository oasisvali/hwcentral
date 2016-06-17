# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0007_auto_20160209_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolprofile',
            name='school',
        ),
        migrations.DeleteModel(
            name='SchoolProfile',
        ),
    ]
