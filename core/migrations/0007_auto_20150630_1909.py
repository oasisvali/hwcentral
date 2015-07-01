# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_auto_20150630_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentquestionslist',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='assignmentquestionslist',
            name='title',
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='number',
            field=models.PositiveIntegerField(default=1,
                                              help_text=b'A positive integer used to disinguish Assignment Questions List for the same topic.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='school',
            field=models.ForeignKey(help_text=b'The school that this Assignment Questions List belongs to.',
                                    to='core.School'),
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='standard',
            field=models.ForeignKey(help_text=b'The standard that this Assignment Questions List is for.',
                                    to='core.Standard'),
        ),
        migrations.AlterField(
            model_name='assignmentquestionslist',
            name='subject',
            field=models.ForeignKey(help_text=b'The subject that this Assignment Questions List is for.',
                                    to='core.Subject'),
        ),
    ]
