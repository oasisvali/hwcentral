from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Chapter, Board, Group, School, UserInfo, Standard, Subject, Home, ClassRoom, SubjectRoom, \
    Question, Assignment, Submission


admin.site.register(Group)
admin.site.register(Board)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Home)
admin.site.register(School)
admin.site.register(UserInfo)
admin.site.register(ClassRoom)
admin.site.register(SubjectRoom)
admin.site.register(Question)
admin.site.register(Assignment)
admin.site.register(Submission)

# Define an inline admin descriptor for UserInfo model
# which acts a bit like a singleton
class UserInfoInline(admin.StackedInline):
    model = UserInfo


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserInfoInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)