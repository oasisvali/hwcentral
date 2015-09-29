# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('concierge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquirer',
            name='phone',
            field=models.CharField(help_text=b'Please enter your contact phone number.', max_length=15, null=True,
                                   blank=True),
        ),
    ]
