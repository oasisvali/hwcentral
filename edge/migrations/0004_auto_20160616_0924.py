# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('edge', '0003_auto_20160123_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectroomquestionmistake',
            name='regression',
            field=models.FloatField(default=0.0,
                                    help_text=b'The absolute value of all the marks lost due to incorrect answers',
                                    validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
