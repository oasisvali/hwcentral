# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_schoolprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='revised',
            field=models.BooleanField(default=False, help_text=b'Has the student completed the revision?'),
        ),
    ]
