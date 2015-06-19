# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='completion',
            field=models.FloatField(help_text=b'Completion (fraction) of this submission.'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='marks',
            field=models.FloatField(help_text=b'Marks (fraction) obtained by this submission.', null=True),
        ),
    ]
