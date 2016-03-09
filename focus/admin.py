# Register your models here.

from django.contrib import admin

# Register your models here.
from focus.models import FocusRoom, Remedial, SchoolProfile

admin.site.register(FocusRoom)
admin.site.register(Remedial)
admin.site.register(SchoolProfile)
