# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_squashed_0009_auto_20150724_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='message',
            field=models.TextField(help_text=b'The textual message to be conveyed to the target.', max_length=1000),
        ),
    ]
