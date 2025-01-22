from rest_framework.response import Response
from scrap.models import result
from .serializers import resultSerializer
from django.shortcuts import render , redirect
from .models import excle_model , excle_model2
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse , Http404
import os
from django.conf import settings
from .utils.extractor import *


# Create your views here.
def file_download(request, file_name):
    try:
        # Construct the file path
        file_path = os.path.join(settings.MEDIA_ROOT, 'excel_files', f'{file_name}.xlsx')

        # Serve the file
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{file_name}.xlsx')
    except FileNotFoundError:
        # If the file doesn't exist, return a 404 error
        raise Http404("File not found")



@login_required(login_url='login')
def download_excel(request, fileName):
    # Fetch file details from the database
    file_details = excle_model.objects.filter(file=f"excel_files/{fileName}.xlsx").first()

    if file_details:
        # Calculate file size in KB
        file_size = round(file_details.file.size / 1024, 2)

        # Pass file information to the template
        file_info = {
            "file_name": fileName,
            "file_size": file_size,
        }
        return render(request, 'data/download.html', file_info)

    # Handle the case where file details are not found
    return render(request, '404.html', {"message": "File not found"})
    



@login_required(login_url='login')
def get_data(request): 
    if request.method == "POST":
        branch = request.POST['branch']
        year = request.POST['year']
        semester = request.POST['semester']
        
        category = '_'.join([f'{branch}',f'{year}',f'{semester}'])
        print(category)    
        
        course = result.objects.filter(user_id = request.user , category = category)
        customer = request.user.id
        print(customer)
        if course.exists():
            print(course)
            serializer = resultSerializer(course, many=True)
            
            filtered_data = serializer.data
            excle_convertor(filtered_data , customer ,branch , year , semester , category)
            
            
            return redirect('d_data' , category)
            
        else:
            messages.error(request , "Data Not Exit, Kindly Scrap That Data")
    
    return render(request , 'data/data_home.html')

