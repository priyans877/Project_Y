from rest_framework.decorators import api_view
from rest_framework.response import Response
from scrap.models import result
from .serializers import resultSerializer
import xlsxwriter
from django.shortcuts import render , redirect
from .models import excle_model , excle_model2
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import xlsxwriter
from io import BytesIO
from django.core.files.base import ContentFile
import json
from django.http import FileResponse
import os
from django.conf import settings


# Create your views here.

def excle_convertor(data, customer):
    # Create an in-memory bytes buffer
    buffer = BytesIO()

    workbook = xlsxwriter.Workbook(buffer, {'in_memory': True})
    worksheet = workbook.add_worksheet('Results')
    
    with open('temp.txt' , 'w') as da:
        da.write(f"{data}")
        
        
    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D3D3D3',
        'border': 1
    })
    
    major_header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#A9A9A9',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    # List of subjects
    subject_code = list(data[0]["result_s"].keys())
    subjects_name = data[0]['result_s'].values()
    sub_name = list(subject_name.get("Subject Name") for subject_name in subjects_name)
    sub_details = {i: {'code': subject_code[i], 'name': sub_name[i]} for i in range(len(subject_code))}
    subjects = list(data[0]["result_s"].keys())
    
    # Write static headers
    worksheet.merge_range('A1:A3', 'Roll No.', header_format)
    worksheet.merge_range('B1:B3', 'Student Name', header_format)
    
    # Write subject headers
    current_col = 2
    for j in sub_details:
        start_col = xlsxwriter.utility.xl_col_to_name(current_col)
        end_col = xlsxwriter.utility.xl_col_to_name(current_col + 3)
        
        worksheet.merge_range(f'{start_col}1:{end_col}1', sub_details[j]['code'], major_header_format)
        worksheet.merge_range(f'{start_col}2:{end_col}2', sub_details[j]['name'], major_header_format)
        
        sub_headers = ['Theory', 'Sessional', 'Practical', 'Total']
        for i, sub_header in enumerate(sub_headers):
            worksheet.write(2, current_col + i, sub_header, header_format)
        
        current_col += 4
    
    # Write student data
    row = 3
    for student in data:
        # Write student info
        worksheet.write(row, 0, student["roll_no"], cell_format)
        worksheet.write(row, 1, student["s_name"], cell_format)
        print(student["roll_no"])
        print(student["s_name"])
        print("-===---===================================")
        
        #Write subject marks
        col = 2
        for subject in subjects:
            
            if subject in student["result_s"]:
                if type(student["result_s"]) == str:
                    try: 
                        temp_data = json.loads(student["result_s"])
                        temp_data = json.loads(temp_data)
                        print("Try completed")
                    except:
                        temp_data = json.loads(student["result_s"])

                    marks =  temp_data[subject]
                    worksheet.write(row, col, marks["Theory"], cell_format)
                    worksheet.write(row, col + 1, marks["Sessional"], cell_format)
                    worksheet.write(row, col + 2, marks["Practical"], cell_format)
                    worksheet.write(row, col + 3, marks["Total Marks"], cell_format)

                else:
                    marks =  student["result_s"][subject]
                    worksheet.write(row, col, marks["Theory"], cell_format)
                    worksheet.write(row, col + 1, marks["Sessional"], cell_format)
                    worksheet.write(row, col + 2, marks["Practical"], cell_format)
                    worksheet.write(row, col + 3, marks["Total Marks"], cell_format)
                    
            else:
                # Fill with empty cells if subject data not available
                worksheet.write(row, col, "", cell_format)
                worksheet.write(row, col + 1, "", cell_format)
                worksheet.write(row, col + 2, "", cell_format)
                worksheet.write(row, col + 3, "", cell_format)
            col += 4
        row += 1
    
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:Z', 12)
    worksheet.set_row(0, 30)
    worksheet.set_row(1, 30)
    worksheet.set_row(2, 30)
    
    workbook.close()
    
    buffer.seek(0)
    
    # Create a Django model instance and save the file
    excel_file = excle_model(user=customer)
    excel_file.file.save('result_sheet2.xlsx', ContentFile(buffer.read()))
    buffer.close()
    print("Excel file created and saved to database successfully!")
    

@login_required(login_url='login')
def download_excel(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'excel_files', 'result_sheet2.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='result_sheet2.xlsx')



@login_required(login_url='login')
def get_data(request): 
    course = result.objects.filter(category = "cse_aiml_21_06")
    serializer = resultSerializer(course, many=True)
    
    filtered_data = serializer.data
    excle_convertor(filtered_data , request.user)
    
    return render(request , "")

