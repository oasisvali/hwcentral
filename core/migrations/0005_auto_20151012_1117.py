# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_auto_20151011_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='number',
            field=models.PositiveIntegerField(default=1,
                                              help_text=b'A positive integer used to disinguish Assignments using the same AssignmentQuestionsList in the same subjectroom.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='chapter',
            field=models.ForeignKey(default=1, to='core.Chapter',
                                    help_text=b'The Chapter that this Assignment Questions List pertains to.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='description',
            field=models.TextField(
                help_text=b'A brief description/listing of the topics covered by this Assignment Question List.',
                max_length=1000),
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='number',
            field=models.PositiveIntegerField(
                help_text=b'A positive integer used to disinguish Assignment Questions List for the same chapter.'),
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='school',
            field=models.ForeignKey(
                help_text=b'The school that this Assignment Questions List belongs to. Use 1 if it belongs to the hwcentral question bank',
                to='core.School'),
        ),
    ]
