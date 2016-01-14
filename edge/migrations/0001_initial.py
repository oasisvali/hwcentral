# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_assignment_completion'),
    ]

    operations = [
        migrations.CreateModel(
                name='Tick',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('mark', models.FloatField(help_text=b'Mark (fraction) obtained for this subpart.',
                                               validators=[django.core.validators.MinValueValidator(0.0),
                                                           django.core.validators.MaxValueValidator(1.0)])),
                    ('question',
                     models.ForeignKey(help_text=b'The question which the target subpart of this tick belongs to.',
                                       to='core.Question')),
                    ('student', models.ForeignKey(help_text=b'The student whose answer resulted in this tick.',
                                                  to=settings.AUTH_USER_MODEL)),
                ],
        ),
    ]
