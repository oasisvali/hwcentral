from django import forms
from django.contrib.auth.models import User
from core.models import Assignment, SubjectRoom, AssignmentQuestionsList, ClassRoom


class AssignmentForm(forms.Form):

    def __init__(self,teacher_id,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
        OPTIONS_LIST =[]
        user = User.objects.get(pk = teacher_id)
        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher_id=teacher_id))
        for subjectroom in SubjectRoom.objects.filter(teacher__id=teacher_id):
            subject_id =subjectroom.subject_id
            for subject in user.subjects_managed_set.all():
                classroom_id = subject.classRoom_id
                standard_id = ClassRoom.objects.get(classroom_id=classroom_id).standard_id
                for assignmentql in AssignmentQuestionsList.filter(subject_id=subject_id,standard_id=standard_id):
                    OPTIONS_LIST.append(str(standard_id)+"_"+str(subject_id),str(subject))
