from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
# Create your views here.




def home(request):
    course = {'name': ["Python"] , "Topic" : ['Python' , 'C++']}
    return  JsonResponse(course)