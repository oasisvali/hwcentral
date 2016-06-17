# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_questionsubpart'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('school', models.OneToOneField(primary_key=True, serialize=False, to='core.School',
                                                help_text=b'The school that this profile is for')),
                ('focus', models.BooleanField(default=False,
                                              help_text=b'Whether the focusrooms feature is enabled for this school')),
                ('pylon', models.BooleanField(default=False,
                                              help_text=b'Whether the sms notification feature is enabled for this school')),
            ],
        ),
    ]
