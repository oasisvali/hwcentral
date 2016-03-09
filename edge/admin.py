# Register your models here.

from django.contrib import admin

# Register your models here.
from edge.models import Tick, StudentProficiency, SubjectRoomProficiency, SubjectRoomQuestionMistake

admin.site.register(Tick)
admin.site.register(StudentProficiency)
admin.site.register(SubjectRoomProficiency)
admin.site.register(SubjectRoomQuestionMistake)
