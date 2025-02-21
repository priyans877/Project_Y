from django.shortcuts import render
from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from data.serializers  import *
from scrap.models import result
from django.shortcuts import render
import json
# Create your views here.


@api_view(['GET' , 'POST'])
def get_result2(request):

    
    if request.method =='POST':
        roll_no = request.data.get("roll_no")

        latest_ids = result.objects.filter(roll_no=roll_no).values('category').annotate(latest_id=Max('id')).values_list('latest_id', flat=True)
        # print(latest_ids)
        result_student = result.objects.filter(id__in=latest_ids).order_by('category')
        # print(result_student)
        data = CategorySerializer(result_student , many = True)
        
        
        student_data ={
            'name' : data.data[0]['s_name'],
            'roll_no' : data.data[0]['roll_no'],
            'category':[],
            'sgpa' : [],
            'total_credits' :[],
            'cgpa' : [],
        }
        
        for student in data.data:
            temp_credit = 0
            student_data['sgpa'].append(float(student['sgpa']) if isinstance(student['sgpa'], (int, float, str)) and str(student['sgpa']).replace('.', '', 1).isdigit() else 0)
            
            student_data['category'].append(student['category'])
            student_data['cgpa'].append(float(student['cgpa']) if student['cgpa'] != '' else 0)
            
            for subject in student['result_s'].values():
                temp_credit+= float(subject["Credits"])
                
            student_data["total_credits"].append(temp_credit)
            # print("------------------------------------------")
           
           
        if max(student_data['cgpa']) == 0:
            sgpa_credit = sum([ a*b  for a , b in zip(student_data['sgpa'] , student_data['total_credits'])])
            credit = sum(student_data['total_credits'])
            cgpa = sgpa_credit/credit
            student_data[cgpa].append(cgpa)
            
            
            
      
        if data:
            return render(request , 'home/result.html',student_data)
        
        

        return Response(f"Got POST Check {roll_no}")
    
    return Response("Got GET method Check")



# def get_result(request):
#     roll_no = "21011018024"
#     latest_ids = result.objects.filter(roll_no=roll_no).values('category').annotate(latest_id=Max('id')).values_list('latest_id', flat=True)
#     # print(latest_ids)
#     result_student = result.objects.filter(id__in=latest_ids).order_by('category')
#     # print(result_student)
#     data = CategorySerializer(result_student , many = True)
    
    
#     student_data ={
#         'name' : data.data[0]['s_name'],
#         'roll_no' : data.data[0]['roll_no'],
#         'category':[],
#         'sgpa' : [],
#         'total_credits' :[],
#         'cgpa' : [],
#     }
    
#     for student in data.data:
#         temp_credit = 0
#         student_data['sgpa'].append(float(student['sgpa']) if isinstance(student['sgpa'], (int, float, str)) and str(student['sgpa']).replace('.', '', 1).isdigit() else 0)
        
#         student_data['category'].append(student['category'])
#         student_data['cgpa'].append(float(student['cgpa']) if student['cgpa'] != '' else 0)
        
#         for subject in student['result_s'].values():
#             temp_credit+= float(subject["Credits"])
            
#         student_data["total_credits"].append(temp_credit)
#         # print("------------------------------------------")
        
        
#     if max(student_data['cgpa']) == 0:
#         sgpa_credit = sum([ a*b  for a , b in zip(student_data['sgpa'] , student_data['total_credits'])])
#         credit = sum(student_data['total_credits'])
#         cgpa = sgpa_credit/credit
#         student_data[cgpa].append(cgpa)
        
        
        
    
#     if data:
#         return render(request , 'home/result.html',student_data)
  
  
  
  
def get_result(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no')
        if roll_no:
            # Get latest results for each category
            latest_ids = result.objects.filter(roll_no=roll_no).values('category').annotate(
                latest_id=Max('id')).values_list('latest_id', flat=True)
            result_student = result.objects.filter(id__in=latest_ids).order_by('category')
            
            if result_student.exists():
                data = CategorySerializer(result_student, many=True)
                
                student_data = {
                    'name': data.data[0]['s_name'],
                    'roll_no': data.data[0]['roll_no'],
                    'father_name' : data.data[0]['f_name'],
                    'branch' : data.data[0]['category'][:-3].upper().replace("_", "/"),                    
                    'category': [],
                    'sgpa': [],
                    'credits': [],
                    'cgpa': [],
                    'MaxSub' : [],
                    'MaxScore': [],
                    'ReCount' : [],
                
                }
                
                for student in data.data:
                    temp_credit = 0
                    student_data['sgpa'].append(
                        float(student['sgpa']) if isinstance(student['sgpa'], (int, float, str)) 
                        and str(student['sgpa']).replace('.', '', 1).isdigit() else 0
                    )
                    
                    student_data['category'].append(student['category'][-1:])
                    student_data['cgpa'].append(float(student['cgpa']) if student['cgpa'] != '' else 0)
                    student_data['ReCount'].append(student['re_count'])  
                    
                    for subject in student['result_s'].values():
                        temp_credit += float(subject["Credits"])
                    
                    sub_res = max(student['result_s'].items(), key=lambda x: x[1]["Theory"])
                    # appending Student having max result subject
                    student_data['MaxSub'].append(sub_res[1]['Subject Name']) 
                    student_data['MaxScore'].append(sub_res[1]["Total Marks"])
                    
        
                    student_data["credits"].append(temp_credit)
                
                
                
                
                
                if student_data['cgpa'][-1] == 0:
                    print("Here")
                    sgpa_credit = sum([a*b for a, b in zip(student_data['sgpa'], student_data['credits'])])
                    credit = sum(student_data['credits'])
                    cgpa = round(sgpa_credit/credit , 3)
                    student_data['cgpa'].append(cgpa)
                    print(credit)

                context = {
                    'solo_result' : student_data,
                    'max_sgpa' : max(student_data['sgpa']),
                    'max_cgpa' : student_data['cgpa'][-1],
                    'total_credits' : sum(student_data['credits']),
                }
                
                print(student_data)
                
                
                
                return render(request, 'marksheet/result.html', context)
            else:
                return render(request, 'marksheet/marksheet_fetch.html', {'error': 'No results found for this roll number'})
    
    # For GET request, just show the form
    return render(request, 'marksheet/marksheet_fetch.html')


  
        