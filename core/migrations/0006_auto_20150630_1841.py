# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_auto_20150623_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'A string descriptor for the question tag.', unique=True, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='subchapter',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='meta',
        ),
        migrations.RemoveField(
            model_name='question',
            name='meta',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subChapters',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='meta',
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='chapter',
            field=models.ForeignKey(default=1, to='core.Chapter',
                                    help_text=b'The chapter that this Assignment Question List covers.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='description',
            field=models.TextField(default='Test AQL Description',
                                   help_text=b'A brief description/listing of the topics covered by this Assignment Question List.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='school',
            field=models.ForeignKey(default=1, to='core.School',
                                    help_text=b'The school that this Assignment Question List belongs to.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='standard',
            field=models.ForeignKey(default=2, to='core.Standard',
                                    help_text=b'The standard that this Assignment Question List is for.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='subject',
            field=models.ForeignKey(default=2, to='core.Subject',
                                    help_text=b'The subject that this Assignment Question List is for.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignmentquestionslist',
            name='title',
            field=models.CharField(default='Test AQL',
                                   help_text=b'A string descriptor for the Assignment Question List.', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SubChapter',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(help_text=b'The set of question tags that this question has been tagged with.',
                                         to='core.QuestionTag'),
        ),
    ]
