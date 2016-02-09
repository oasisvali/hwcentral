# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0002_schoolprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='schoolprofile',
            name='school',
            field=models.OneToOneField(primary_key=True, serialize=False, to='core.School',
                                       help_text=b'The school that this focus profile is for'),
        ),
    ]
