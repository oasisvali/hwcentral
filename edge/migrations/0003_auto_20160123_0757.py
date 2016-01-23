# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_assignment_completion'),
        ('edge', '0002_auto_20160114_2026'),
    ]

    operations = [
        migrations.CreateModel(
                name='StudentProficiency',
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
                    ('total', models.FloatField(default=0.0,
                                                help_text=b'Total tick marks that the user has obtained in this questiontag',
                                                validators=[django.core.validators.MinValueValidator(0.0)])),
                    ('ticks', models.PositiveIntegerField(default=0,
                                                          help_text=b'The number of ticks that this proficiency has been calculated over')),
                    ('questiontag', models.ForeignKey(help_text=b'The tag that the proficiency is being calculated in.',
                                                      to='core.QuestionTag')),
                    ('student', models.ForeignKey(help_text=b'The student whose proficieny is being logged.',
                                                  to=settings.AUTH_USER_MODEL)),
                    ('subjectRoom', models.ForeignKey(
                        help_text=b"The subjectroom whose student's proficiency or average proficiency is being recorded",
                        to='core.SubjectRoom')),
                ],
                options={
                    'abstract': False,
                },
        ),
        migrations.CreateModel(
                name='SubjectRoomQuestionMistake',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('regression', models.FloatField(default=0.0,
                                                     help_text=b'Abslute value of all the marks lost due to incorrect answers',
                                                     validators=[django.core.validators.MinValueValidator(0.0)])),
                    ('question', models.ForeignKey(
                        help_text=b'The question for which incorrect answers are tallied to create this record',
                        to='core.Question')),
                    ('subjectRoom', models.ForeignKey(
                        help_text=b'The subjectroom whose students have made the question mistakes which are being aggregated',
                        to='core.SubjectRoom')),
                ],
        ),
        migrations.RemoveField(
                model_name='proficiency',
                name='questiontag',
        ),
        migrations.RemoveField(
                model_name='proficiency',
                name='student',
        ),
        migrations.AddField(
                model_name='tick',
                name='subjectRoom',
                field=models.ForeignKey(default=3, to='core.SubjectRoom',
                                        help_text=b"The subjectroom whose assignment's submission contains this tick"),
                preserve_default=False,
        ),
        migrations.AlterField(
                model_name='subjectroomproficiency',
                name='questiontag',
                field=models.ForeignKey(help_text=b'The tag that the proficiency is being calculated in.',
                                        to='core.QuestionTag'),
        ),
        migrations.AlterField(
                model_name='subjectroomproficiency',
                name='subjectRoom',
                field=models.ForeignKey(
                    help_text=b"The subjectroom whose student's proficiency or average proficiency is being recorded",
                    to='core.SubjectRoom'),
        ),
        migrations.DeleteModel(
                name='Proficiency',
        ),
    ]
