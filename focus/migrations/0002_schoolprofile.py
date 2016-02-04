# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_remove_assignment_subjectroom'),
        ('focus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
                name='SchoolProfile',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('focusRoom', models.BooleanField(default=True,
                                                      help_text=b'Whether the focusroom feature is enabled for this school')),
                    ('school',
                     models.OneToOneField(to='core.School', help_text=b'The school that this focus profile is for')),
                ],
        ),
    ]
