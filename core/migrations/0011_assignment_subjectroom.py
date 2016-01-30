# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_remove_assignment_subjectroom'),
    ]

    operations = [
        migrations.AddField(
                model_name='assignment',
                name='subjectRoom',
                field=models.ForeignKey(default=8, to='core.SubjectRoom',
                                        help_text=b'The subjectroom that this assignment is assigned to.'),
                preserve_default=False,
        ),
    ]
