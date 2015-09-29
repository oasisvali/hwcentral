# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_auto_20150817_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='admin',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL,
                                       help_text=b'The admin user who manages this school.'),
        ),
    ]
