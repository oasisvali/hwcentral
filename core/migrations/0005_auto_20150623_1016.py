# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_auto_20150623_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='average',
            field=models.FloatField(blank=True, help_text=b'Subjectroom average (fraction) for this assignment.',
                                    null=True, validators=[django.core.validators.MinValueValidator(0.0),
                                                           django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='marks',
            field=models.FloatField(blank=True, help_text=b'Marks (fraction) obtained by this submission.', null=True,
                                    validators=[django.core.validators.MinValueValidator(0.0),
                                                django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
