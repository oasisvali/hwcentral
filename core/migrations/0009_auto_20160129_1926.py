# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from core.models import CORE_APP_LABEL


def set_object_id(apps, schema_editor):
    # We can't import the Assignment model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Assignment = apps.get_model(CORE_APP_LABEL, "Assignment")
    for assignment in Assignment.objects.all():
        assignment.object_id = assignment.subjectRoom.pk
        assignment.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_auto_20160129_1925'),
    ]

    operations = [
        migrations.RunPython(set_object_id)
    ]
