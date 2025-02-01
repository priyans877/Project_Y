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
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='login')
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
    print(fileName)
    course = result.objects.filter(user_id = request.user.id , category = fileName).order_by('s_name')
    customer = request.user.id
    semester = semester_filter([fileName])
    year = extract_year([fileName])
    branch = branch_filter([fileName])
    print(course)
    print(customer)
    
    if course.exists():
        print(course)
        serializer = resultSerializer(course, many=True)
        
        filtered_data = serializer.data
        excelfile = excle_convertor(filtered_data , customer ,branch[0] , year[0] , semester[0] , fileName)
        print(excelfile)
    
    # print("after if condition")
    # print(fileName)
    if request.user.is_superuser:
        file_details = excle_model.objects.filter(file__startswith=f"excel_files/{fileName}").first()
    else:
        file_details = excle_model.objects.filter(
            file__startswith=f"excel_files/{fileName}", user_id=request.user.id
        ).first()
        
    print(file_details)

    if file_details:
    
        # Calculate file size in KB
        print(file_details.file.url)
        file_size = round(file_details.file.size / 1024, 2)

        # Pass file information to the template
        file_info = {
            "file_name": fileName,
            "file_size": file_size,
        }
        print(file_info)
        return render(request, 'data/download.html', file_info)

    # Handle the case where file details are not found
    return JsonResponse({"message": "you dont have data , so Kindly scrap"})
    
    
    s
@login_required(login_url='login')
def data_view(request):
    # Fetch all results initially
    course = result.objects.filter(user_id = request.user.id)
    # Extract filtering options from the data
    semester_options = set(semester_filter([p.category for p in course]))
    year_options = set(extract_year([p.category for p in course]))
    branch_options = set(branch_filter([p.category for p in course]))

   
    selected_sem = request.GET.get('selected_sem', '')
    selected_year = request.GET.get('selected_year', '')
    selected_branch = request.GET.get('selected_branch', '')
    
    
    if selected_sem or selected_year or selected_branch:
        
        # Start filtering the `course` queryset
        if selected_sem:
            course = course.filter(category__icontains=selected_sem)

        if selected_year:
            course = course.filter( category__icontains=selected_year)

        if selected_branch:
            course = course.filter(category__icontains=selected_branch)


  
        # Extract options dynamically based on the filtered data
        semester_options = set(extract_year([p.category for p in course]))
        year_options = set(extract_year([p.category for p in course]))
        branch_options = set(branch_filter([p.category for p in course]))
        
    # Handle the case where all three filters are selected
    if selected_sem and selected_year and selected_branch:
        print("_".join([selected_branch, selected_year, semester_filter_s(selected_sem)]))
        # Perform strict filtering for the specific combination
        course = result.objects.filter(
            category="_".join([selected_branch, selected_year, semester_filter_s(selected_sem)]),
            user_id = request.user.id
        )

    # HTMX-specific response
    if request.headers.get('HX-Request'):
        return render(request, 'data/partial_data.html', {"datas": course})

    # Full page response
    return render(request, 'data/data.html', {
        "datas": course,
        "sem_options": semester_options,
        "year_options": year_options,
        "branch_options": branch_options,
    })




# @login_required(login_url='login')
# def get_data(request): 
#     if request.method == "POST":
#         branch = request.POST['branch']
#         year = request.POST['year']
#         semester = request.POST['semester']
        
#         category = '_'.join([f'{branch}',f'{year}',f'{semester}'])
#         print(category)    
        
    #     course = result.objects.filter(user_id = request.user , category = category)
    #     customer = request.user.id
    #     print(customer)
    #     if course.exists():
    #         print(course)
    #         serializer = resultSerializer(course, many=True)
            
    #         filtered_data = serializer.data
    #         excle_convertor(filtered_data , customer ,branch , year , semester , category)
            
            
    #         return redirect('d_data' , category)
            
    #     else:
    #         messages.error(request , "Data Not Exit, Kindly Scrap That Data")
    
    # return render(request , 'data/data_home.html')

