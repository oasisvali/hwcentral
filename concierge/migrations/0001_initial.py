# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enquirer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Please enter your name.', max_length=255)),
                ('email', models.EmailField(help_text=b'Please enter your email address.', max_length=255)),
                ('school', models.CharField(help_text=b'Please enter your school/organization.', max_length=255)),
                ('phone', models.CharField(help_text=b'Please enter your contact phone number.', max_length=15)),
            ],
        ),
    ]
