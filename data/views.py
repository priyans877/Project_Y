from rest_framework.response import Response
from scrap.models import result
from .serializers import resultSerializer
from django.shortcuts import render , redirect
from .models import excle_model , excle_model2
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import os
from django.conf import settings
from .utils.extractor import *


# Create your views here.



@login_required(login_url='login')
def download_excel(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'excel_files', 'result_sheet2.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='result_sheet2.xlsx')



@login_required(login_url='login')
def get_data(request): 
    if request.method == "POST":
        branch = request.POST['branch']
        year = request.POST['year']
        semester = request.POST['semester']
        
        category = '_'.join([f'{branch}',f'{year}',f'{semester}'])
        print(category)    
        
        course = result.objects.filter(user_id = request.user , category = category)
        
        if course.exists():
            print(course)
            # serializer = resultSerializer(course, many=True)
            
            # filtered_data = serializer.data
            # excle_convertor(filtered_data , request.user)
        else:
            messages.error(request , "Data Not Exit, Kindly Scrap That Data")
    
    return render(request , 'data/data_home.html')

