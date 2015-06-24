# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import relativefilepathfield.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_auto_20150619_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentQuestionsList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='questions',
        ),
        migrations.AddField(
            model_name='assignment',
            name='average',
            field=models.FloatField(help_text=b'Subjectroom average (fraction) for this assignment.', null=True,
                                    validators=[django.core.validators.MinValueValidator(0.0),
                                                django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='meta',
            field=relativefilepathfield.fields.RelativeFilePathField(
                help_text=b"Path to this assignment's metadata file.", path=b'/Users/oasis/hwcentral/core/assignments',
                max_length=255, match=b'\\d+.json'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='subjectRoom',
            field=models.ForeignKey(help_text=b'The subjectroom that this assignment is assigned to.',
                                    to='core.SubjectRoom'),
        ),
        migrations.AlterField(
            model_name='home',
            name='parent',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL,
                                       help_text=b'The parent user for whom the home is defined.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='meta',
            field=relativefilepathfield.fields.RelativeFilePathField(
                help_text=b"Path to this question's metadata file.", path=b'/Users/oasis/hwcentral/core/questions',
                max_length=255, match=b'\\d+.json'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='completion',
            field=models.FloatField(help_text=b'Completion (fraction) of this submission.',
                                    validators=[django.core.validators.MinValueValidator(0.0),
                                                django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='marks',
            field=models.FloatField(help_text=b'Marks (fraction) obtained by this submission.', null=True,
                                    validators=[django.core.validators.MinValueValidator(0.0),
                                                django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='meta',
            field=relativefilepathfield.fields.RelativeFilePathField(
                help_text=b"Path to this submission's metadata file.", path=b'/Users/oasis/hwcentral/core/submissions',
                max_length=255, match=b'\\d+.json'),
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='questions',
            field=models.ManyToManyField(help_text=b'The set of questions that make up an assignment.',
                                         to='core.Question'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='assignmentQuestionsList',
            field=models.ForeignKey(default=1, to='core.AssignmentQuestionsList',
                                    help_text=b'The list of questions that make up this assignment.'),
            preserve_default=False,
        ),
    ]
