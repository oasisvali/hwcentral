# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ink', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossier',
            name='phone',
            field=models.CharField(help_text=b'Primary contact phone number for the user', max_length=10),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='secondaryPhone',
            field=models.CharField(help_text=b'Secondary contact phone number for the user', max_length=12, null=True, blank=True),
        ),
    ]
