from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

def land(request):
	return HttpResponse('Looking at Land')

def register(request):
	return HttpResponse('Looking at Register')

def login(request):
	return HttpResponse('Looking at Login')

def classroom(request, id=None):
	return HttpResponse('Looking at Classroom')

def hw(request, id=None):
	return HttpResponse('Looking at Hw')

def submission(request, id=None):
	return HttpResponse('Looking at Submission')

def user(request, id=None):
	return HttpResponse('Looking at User')

def school(request, id=None):
	return HttpResponse('Looking at School. Id is: ' + str(id))

def board(request, id=None):
	return HttpResponse('Looking at Board')