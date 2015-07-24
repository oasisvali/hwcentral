from django import forms

from core.models import ClassRoom, SubjectRoom, MAX_TEXTFIELD_LENGTH

ANNOUNCEMENT_TARGET_HELP_TEXT = "Select the class where you would like to make this announcement"

class BaseAnnouncementForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(BaseAnnouncementForm,self).__init__(*args,**kwargs)
    message = forms.CharField(widget=forms.Textarea ,
                              max_length=MAX_TEXTFIELD_LENGTH,
                              help_text='Enter the message you wish to display in the announcement'
                                        '. %s characters max.' % MAX_TEXTFIELD_LENGTH)

class AdminAnnouncementForm(BaseAnnouncementForm):
    pass
class ClassAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(ClassAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.filter(classTeacher=classteacher),
                                                          help_text=ANNOUNCEMENT_TARGET_HELP_TEXT)

class SubjectAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(SubjectAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=classteacher),
                                                           help_text=ANNOUNCEMENT_TARGET_HELP_TEXT)

class ClassSubjectAnnouncementForm(BaseAnnouncementForm):
    # These are used to differentiate between classroom and subjectroom model selections
    CLASSROOM_ID_PREFIX = "classroom"
    SUBJECTROOM_ID_PREFIX = "subjectroom"

    def __init__(self,classteacher,*args,**kwargs):
        super(ClassSubjectAnnouncementForm,self).__init__(*args,**kwargs)
        options_list =[]
        for subjectroom in SubjectRoom.objects.filter(teacher=classteacher):
            options_list.append(
                (ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX + str(subjectroom.pk), str(subjectroom)))
        for classroom in ClassRoom.objects.filter(classTeacher=classteacher):
            options_list.append(
                (ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX + str(classroom.pk), str(classroom)))
        self.fields['target'] = forms.ChoiceField(choices=options_list,
                                                  help_text=ANNOUNCEMENT_TARGET_HELP_TEXT)



