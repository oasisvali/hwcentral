# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0007_assignment_completion'),
    ]

    operations = [
        migrations.AddField(
                model_name='assignment',
                name='content_type',
                field=models.ForeignKey(default=18, to='contenttypes.ContentType',
                                        help_text=b'The type of the target of this assignment.'),
                preserve_default=False,
        ),
        migrations.AddField(
                model_name='assignment',
                name='object_id',
                field=models.PositiveIntegerField(default=1,
                                                  help_text=b'The primary key of the target of this assignment.'),
                preserve_default=False,
        ),
    ]
