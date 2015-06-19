# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_auto_20150618_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='content_type',
            field=models.ForeignKey(help_text=b'The type of the target of this announcement.',
                                    to='contenttypes.ContentType'),
        ),
    ]
