# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0005_auto_20160209_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='focusroom',
            name='id',
        ),
        migrations.AlterField(
            model_name='focusroom',
            name='subjectRoom',
            field=models.OneToOneField(primary_key=True, serialize=False, to='core.SubjectRoom',
                                       help_text=b'The subjectroom that this focusroom is for'),
        ),
    ]
