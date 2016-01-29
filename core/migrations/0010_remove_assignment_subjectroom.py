# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_auto_20160129_1926'),
    ]

    operations = [
        migrations.RemoveField(
                model_name='assignment',
                name='subjectRoom',
        ),
    ]
