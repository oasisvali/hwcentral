# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151012_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='timestamp',
            field=models.DateTimeField(help_text=b'Timestamp of when this submission was submitted.'),
        ),
    ]
