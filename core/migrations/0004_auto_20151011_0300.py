# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20150922_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='announcer',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL,
                                    help_text=b'The user who made this announcement'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='school',
            field=models.ForeignKey(
                help_text=b'The school question bank that this question belongs to. Use 1 if it belongs to the hwcentral question bank.',
                to='core.School'),
        ),
    ]
