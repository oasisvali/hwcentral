# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_remove_assignment_subjectroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSubpart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(
                    help_text=b'The index of this subpart in the ordering of all subparts for its parent question.')),
                ('question',
                 models.ForeignKey(help_text=b'The question that this subpart belongs to.', to='core.Question')),
                ('tags',
                 models.ManyToManyField(help_text=b'The set of question tags that this subpart has been tagged with.',
                                        to='core.QuestionTag')),
            ],
        ),
    ]
