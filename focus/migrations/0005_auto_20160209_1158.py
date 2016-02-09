# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def update_remedial_foreign_keys(apps, schema_editor):
    # We can't import the Remedial model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    focus_app_label = 'focus'
    Remedial = apps.get_model(focus_app_label, "Remedial")
    FocusRoom = apps.get_model(focus_app_label, "FocusRoom")
    for remedial in Remedial.objects.all():
        remedial.focusRoom = (FocusRoom.objects.get(pk=remedial.focusRoom)).subjectRoom.pk
        remedial.save()


class Migration(migrations.Migration):
    dependencies = [
        ('focus', '0004_auto_20160209_1157'),
    ]

    operations = [
        migrations.RunPython(update_remedial_foreign_keys)
    ]
