# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_assignment_completion'),
        ('edge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
                name='Proficiency',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('total', models.FloatField(default=0.0,
                                                help_text=b'Total tick marks that the user has obtained in this questiontag',
                                                validators=[django.core.validators.MinValueValidator(0.0)])),
                    ('ticks', models.PositiveIntegerField(default=0,
                                                          help_text=b'The number of ticks that this proficieny has been calculated over')),
                    ('rate', models.FloatField(default=0.0, help_text=b'The proficiency rate in this questiontag',
                                               validators=[django.core.validators.MinValueValidator(0.0),
                                                           django.core.validators.MaxValueValidator(1.0)])),
                    ('percentile', models.FloatField(default=0.0,
                                                     help_text=b'The percentile value (as a Fraction) for this proficiency',
                                                     validators=[django.core.validators.MinValueValidator(0.0),
                                                                 django.core.validators.MaxValueValidator(1.0)])),
                    ('score', models.FloatField(default=0.0,
                                                help_text=b'The final score that this proficiency is compared by (as a Fraction)',
                                                validators=[django.core.validators.MinValueValidator(0.0),
                                                            django.core.validators.MaxValueValidator(1.0)])),
                    ('questiontag', models.ForeignKey(help_text=b'The tag that the proficiency is being calculated in.',
                                                      to='core.QuestionTag')),
                    ('student', models.ForeignKey(help_text=b'The student whose proficieny is being logged.',
                                                  to=settings.AUTH_USER_MODEL)),
                ],
        ),
        migrations.CreateModel(
                name='SubjectRoomProficiency',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('rate', models.FloatField(default=0.0, help_text=b'The proficiency rate in this questiontag',
                                               validators=[django.core.validators.MinValueValidator(0.0),
                                                           django.core.validators.MaxValueValidator(1.0)])),
                    ('percentile', models.FloatField(default=0.0,
                                                     help_text=b'The percentile value (as a Fraction) for this proficiency',
                                                     validators=[django.core.validators.MinValueValidator(0.0),
                                                                 django.core.validators.MaxValueValidator(1.0)])),
                    ('score', models.FloatField(default=0.0,
                                                help_text=b'The final score that this proficiency is compared by (as a Fraction)',
                                                validators=[django.core.validators.MinValueValidator(0.0),
                                                            django.core.validators.MaxValueValidator(1.0)])),
                    ('questiontag', models.ForeignKey(to='core.QuestionTag')),
                    ('subjectRoom', models.ForeignKey(to='core.SubjectRoom')),
                ],
        ),
        migrations.AddField(
                model_name='tick',
                name='ack',
                field=models.BooleanField(default=False,
                                          help_text=b'Whether this tick has been acknowledged while calculating proficiency'),
        ),
    ]
