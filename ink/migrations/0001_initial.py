# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL,
                                              help_text=b'The user object that this dossier is associated with.')),
                ('secondaryEmail',
                 models.EmailField(help_text=b'Secondary contact email for the user', max_length=254, null=True,
                                   blank=True)),
                ('flagged', models.BooleanField(help_text=b'Is this user flagged for follow-up?')),
                ('phone', models.CharField(help_text=b'Primary contact phone number for the user', max_length=15)),
                ('secondaryPhone',
                 models.CharField(help_text=b'Secondary contact phone number for the user', max_length=15, null=True,
                                  blank=True)),
            ],
        ),
    ]
