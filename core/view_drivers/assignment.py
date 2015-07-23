from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from core.forms.assignment import AssignmentForm
from core.models import Assignment, AssignmentQuestionsList, SubjectRoom
from django  import forms
import datetime
from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment import AssignmentBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar


def validate_password(form):
        assigned = form.cleaned_data['assigned']
        due = form.cleaned_data['due']
        assigned_date = assigned.date()
        assigned_time = assigned.time()
        due_date = due.date()
        due_time = due.time()
        today = datetime.date.today()
        now = datetime.datetime.now()
        if  assigned_date != today:
            raise forms.ValidationError("The assigment must be assigned today! ")

        if assigned_time > (now-datetime.timedelta(seconds=70)).time():
            raise forms.ValidationError(" The time when assigment is assigned is invalid! ")
        if due_date<assigned_date:
            raise forms.ValidationError(" An assignment cant be due before it has been assigned! ")
        if due_date< today + datetime.timedelta(1):
            raise forms.ValidationError(" Every assignment must at least have a day before it's due ")
        return

class AssignmentDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(AssignmentDriver, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT

    def student_endpoint(self):
        return HttpResponseNotFound()

    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        return HttpResponseNotFound()


class AssignmentGet(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user)
        return render(self.request, UrlNames.ASSIGNMENT.get_template(),AuthenticatedBase(TeacherSidebar(self.user),AssignmentBody(form))
                      .as_context() )


class AssignmentPost(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user,self.request.POST)
        if form.is_valid():
            validate_password(form)
            aqllist= form.cleaned_data['questionlists'].split('_')
            assignmentQuestionsList = AssignmentQuestionsList.objects.get(id=aqllist[3])
            subjectRoom = SubjectRoom.objects.get(id =form.cleaned_data['subjectroom'].id)
            assigned = form.cleaned_data['assigned']
            due = form.cleaned_data['due']
            Assignment.objects.create(assignmentQuestionsList=assignmentQuestionsList,subjectRoom=subjectRoom,assigned=assigned,due=due)
            return redirect(UrlNames.HOME.name)
        else:
            return render(self.request, UrlNames.ASSIGNMENT.get_template(),
                          AuthenticatedBase(TeacherSidebar(self.user),AssignmentBody(form)).as_context() )
