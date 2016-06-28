# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_submission_revised'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenStudentHighest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student', models.ForeignKey(help_text=b'The open student user who has achieved this high mark.',
                                              to=settings.AUTH_USER_MODEL)),
                ('submission',
                 models.ForeignKey(help_text=b'Submission with the highest marks (unique for every question set)',
                                   to='core.Submission')),
            ],
        ),
    ]
