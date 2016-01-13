# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_auto_20151123_1245'),
    ]

    operations = [
        migrations.AddField(
                model_name='assignment',
                name='completion',
                field=models.FloatField(blank=True,
                                        help_text=b'Completion rate (fraction) over the entire subjectroom for this assignment.',
                                        null=True, validators=[django.core.validators.MinValueValidator(0.0),
                                                               django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
