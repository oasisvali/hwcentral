from django import forms

from core.forms.fields import CustomLabelModelChoiceField
from core.forms.widgets import ChosenNoSearchSelect
from core.models import ClassRoom, SubjectRoom, MAX_TEXTFIELD_LENGTH
from core.utils.labels import get_subjectroom_label, get_classroom_label

ANNOUNCEMENT_TARGET_HELP_TEXT = "Select the class where you would like to make this announcement"

class BaseAnnouncementForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea ,
                              max_length=MAX_TEXTFIELD_LENGTH,
                              help_text='Enter the message you wish to display in the announcement'
                                        '. %s characters max.' % MAX_TEXTFIELD_LENGTH)

class AdminAnnouncementForm(BaseAnnouncementForm):
    def __init__(self, *args, **kwargs):
        super(AdminAnnouncementForm, self).__init__(*args, **kwargs)
        # customize the help text
        self.fields['message'].help_text += ' This announcement will be made to the entire school.'

class ClassAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(ClassAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['classroom'] = CustomLabelModelChoiceField(get_classroom_label, queryset=ClassRoom.objects.filter(classTeacher=classteacher),
                                                               widget=ChosenNoSearchSelect,
                                                               help_text=ANNOUNCEMENT_TARGET_HELP_TEXT,
                                                               empty_label=None)

class SubjectAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(SubjectAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['subjectroom'] = CustomLabelModelChoiceField(get_subjectroom_label, queryset=SubjectRoom.objects.filter(teacher=classteacher),
                                                                 widget=ChosenNoSearchSelect,
                                                                 help_text=ANNOUNCEMENT_TARGET_HELP_TEXT,
                                                                 empty_label=None)

class ClassSubjectAnnouncementForm(BaseAnnouncementForm):
    # These are used to differentiate between classroom and subjectroom model selections
    CLASSROOM_ID_PREFIX = "classroom"
    SUBJECTROOM_ID_PREFIX = "subjectroom"

    def __init__(self,classteacher,*args,**kwargs):
        super(ClassSubjectAnnouncementForm,self).__init__(*args,**kwargs)
        options_list =[]
        for subjectroom in SubjectRoom.objects.filter(teacher=classteacher):
            options_list.append(
                (ClassSubjectAnnouncementForm.CLASSROOM_ID_PREFIX + str(subjectroom.pk), get_subjectroom_label(subjectroom)))
        for classroom in ClassRoom.objects.filter(classTeacher=classteacher):
            options_list.append(
                (ClassSubjectAnnouncementForm.SUBJECTROOM_ID_PREFIX + str(classroom.pk), get_classroom_label(classroom)))
        self.fields['target'] = forms.ChoiceField(choices=options_list, widget=ChosenNoSearchSelect,
                                                  help_text=ANNOUNCEMENT_TARGET_HELP_TEXT)



