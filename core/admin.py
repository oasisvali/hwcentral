from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Chapter, Board, Group, School, UserInfo, Standard, Subject, Home, ClassRoom, SubjectRoom, \
    Question, Assignment, Submission, Announcement, AssignmentQuestionsList, QuestionTag, QuestionSubpart, SchoolProfile
from ink.models import Dossier

admin.site.register(Group)
admin.site.register(Board)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(QuestionTag)
admin.site.register(Home)
admin.site.register(School)
admin.site.register(ClassRoom)
admin.site.register(SubjectRoom)
admin.site.register(Question)
admin.site.register(QuestionSubpart)
admin.site.register(AssignmentQuestionsList)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Announcement)

# Define an inline admin descriptor for UserInfo model
# which acts a bit like a singleton
class UserInfoInline(admin.StackedInline):
    model = UserInfo


class DossierInline(admin.StackedInline):
    model = Dossier

# Define a new User admin
class TotalUserAdmin(UserAdmin):
    inlines = (UserInfoInline, DossierInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, TotalUserAdmin)


class SchoolProfileInline(admin.StackedInline):
    model = SchoolProfile


# Define a new User admin
class SchoolAdmin(ModelAdmin):
    inlines = (SchoolProfileInline,)


# Re-register UserAdmin
admin.site.unregister(School)
admin.site.register(School, SchoolAdmin)
