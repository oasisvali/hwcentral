from django.forms import ModelForm
from core.models import Assignment


class AssignmentForm(ModelForm):
    def __init__(self,teacher_id,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
    class Meta:
        model = Assignment
        exclude = ('average',)