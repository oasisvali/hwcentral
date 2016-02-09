# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0003_auto_20160209_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remedial',
            name='focusRoom',
            field=models.PositiveIntegerField(help_text=b'The focusroom that this remedial is assigned to'),
        ),
    ]
