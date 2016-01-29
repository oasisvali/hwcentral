# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_remove_assignment_subjectroom'),
    ]

    operations = [
        migrations.CreateModel(
                name='FocusRoom',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('subjectRoom', models.OneToOneField(to='core.SubjectRoom',
                                                         help_text=b'The subjectroom that this focusroom is for')),
                ],
        ),
        migrations.CreateModel(
                name='Remedial',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('focusRoom', models.ForeignKey(help_text=b'The focusroom that this remedial is assigned to',
                                                    to='focus.FocusRoom')),
                    ('students',
                     models.ManyToManyField(help_text=b'The set of students that have been assigned this remedial',
                                            related_name='remedials_enrolled_set', to=settings.AUTH_USER_MODEL)),
                ],
        ),
    ]
