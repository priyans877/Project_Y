from ..models import excle_model
import xlsxwriter
from io import BytesIO
from django.core.files.base import ContentFile
import json



def excle_convertor(data, customer ,branch , year , semester_s ,category):
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
    try :
        try:
            excel_file = excle_model.objects.get(user_id=customer , file = f"excel_files/{category}.xlsx")
            print(customer)
            if excel_file.exists():
                print("FIle Already Exists")
                pass
        except:
            pass
        
        try:
            print(customer , branch , year , semester_filter_s(semester_s)  , f"excel_files/{category}.xlsx")
            excel_file, created = excle_model.objects.update_or_create(
                user_id=customer,
                branch=branch,
                year=year,
                semester=semester_filter_s(semester_s),
                defaults={"file": f'excel_files/{category}.xlsx'},
            )

            # Save the file content
            excel_file.file.save(f"{category}.xlsx", ContentFile(buffer.read()))

            # Close the buffer after saving
            buffer.close()

            # Optional logging/debugging
            if created:
                print("New object created.")
            else:
                print("Existing object updated.")
        except:
            pass
    except:
        pass
        
       
    
        
    return f'excel_files/{category}.xlsx'


def branch_filter(data):
    for i in range(len(data)):
        if len(data[i])==10:
            data[i] = "mech"
        if len(data[i])== 9:
            if data[i][:1]=="m" :
                data[i] = "mba"
            else :
                data[i] = "bba"
        if len(data[i])== 11:
            if data[i][:1]=="c" :
                data[i] = "civil"
            else :
                data[i] = "bba_f"
        if len(data[i]) ==13:
            if data[i][:1] == "c":
                data[i] = 'cse_gen'
            else:
                data[i] = 'bca_gen'
        if len(data[i]) ==12:
            data[i] = 'bca_ds'
        if len(data[i])==14:
            data[i] = 'cse_aiml'
    return data


def semester_filter(datax):
    data = datax
    for i in range(len(data)):
      
        if data[i][-2:] == "01":
            data[i] = "First Semester"
        elif data[i][-2:] == "02":
            data[i] = "Second Semester"
        elif data[i][-2:] == "03":
            data[i] = "Third Semester"
        elif data[i][-2:] == "04":
            data[i] = "Fourth Semester"
        elif data[i][-2:] == "05":
            data[i] = "Fifth Semester"
        elif data[i][-2:] == "06":
            data[i] = "Sixth Semester"
        elif data[i][-2:] == "07":
            data[i] = "Seventh Semester"
        else:
            data[i] = "Eight Semester"
            
    return data


def semester_filter_s(value):
    if value == "First Semester":
        return "01"
    elif value == "Second Semester":
        return "02"
    elif value == "Third Semester":
        return "03"
    elif value == "Fourth Semester":
        return "04"
    elif value == "Fifth Semester":
        return "05"
    elif value == "Sixth Semester":
        return "06"
    elif value == "Seventh Semester":
        return "07"
    elif value == "Eighth Semester":
        return "08"


def extract_year(texts):
    for i in range(len(texts)):
        parts = texts[i].split('_')
        for part in parts:
            if part.isdigit() and len(part) == 2 and int(part) >8:
                texts[i] = part
    return texts



    