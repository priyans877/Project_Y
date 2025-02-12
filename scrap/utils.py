from django.conf import settings
from .models import *
import json
from bs4 import BeautifulSoup
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import tempfile
import requests

load_dotenv()

media_path = settings.MEDIA_URL

print(media_path , end="")
def subject_parse(soup):
    subject_code= []
    subject_name = []
    credit = []
    theory = []
    sessional = []
    practicle = []
    pass_s = []

    for i in range(16 , 150 , 8):
        try:
            table = "".join(soup.select('tr')[i].select('td')[2].text.split())
            subject_code.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[3].text.split())
            subject_name.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[4].text.split())
            credit.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[14].text.split())
            theory.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[16].text.split())
            sessional.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[18].text.split())
            practicle.append(table)
            # print("------------------------------------------------")
            table = " ".join(soup.select('tr')[i].select('td')[19].text.split())
            pass_s.append(table)
        except: pass
    theory = [x if x != "NA" and x != "" else "0" for x in theory]
    sessional = [x if x != "NA" and x != "" else "0" for x in sessional]
    practicle = [x if x != "NA" and x != "" else "0" for x in practicle]
    total_marks = list(map(lambda x, y , z: int(x) + int(y) +int(z), theory, sessional , practicle))
    

    result_s ={
    "subject_code": subject_code,
    "subject_name": subject_name,
    "credit": credit,
    "theory": theory,
    "sessional": sessional,
    "practicle": practicle,
    "total_marks": total_marks,
    "pass_s": pass_s
    }

    result_s = json.dumps(result_s)
    result_s = json.loads(result_s)
    subjects = {}
    
    for i in range(len(result_s["subject_code"])):
        subject_code = result_s["subject_code"][i]
        subjects[subject_code] = {
            "Subject Name": result_s["subject_name"][i],
            "Credits": result_s["credit"][i],
            "Theory": int(result_s["theory"][i]) if result_s["theory"][i] else 0,
            "Sessional": int(result_s["sessional"][i]),
            "Practical": int(result_s["practicle"][i]) if result_s["practicle"][i] else 0,
            "Total Marks": result_s["total_marks"][i],
            "Grade": result_s["pass_s"][i]
        }
        
    # print(subjects)
    return json.dumps(subjects)

def data_save(current_state, page_s , user_detail):
    count = ''
    try:
        batch = current_state['batch']
        branch = current_state['branch']
        roll_no = current_state['roll_no']
        semester_cat = current_state['semester']
        
        data_id = "_".join([branch ,batch , semester_cat]) 
        
        soup = BeautifulSoup(page_s, 'html.parser')
        
        student_name = soup.find(id ="lblname").text
        
        roll = soup.find(id = "lblRollNo").text
        
        mother_name = soup.find(id = "lblMotherName").text

        father_name = soup.find(id = "lblFatherName").text
        
        sgpaS = soup.find(id = "lblResult").text
        re_appear_count = ''

        try :
            if isinstance(float(sgpaS) , float):
                # print("True integer")
                sgpa = float(sgpaS)
                re_appear_count = 0
                # print(re_appear_count , sgpaS)
        except:
            sgpaS = sgpaS.split()
            re_appear_count = len(sgpaS)
            
            # print(re_appear_count , sgpaS)
            # print("Not an integer")
                    
        c_result = soup.find(id = "lblCgpaResult").text
        
        # print("Here before process_Sub_result")
        
        #EVERYTHING FINE TILL HERE
        sub_result =  json.loads(subject_parse(soup))
        # print("Here after process_sgpa")
        
        # print("here " , student_name,roll,father_name,mother_name,data_id,sgpaS,c_result ,re_appear_count , sub_result)
        # print("Here after process_sgpa")
        
        result_entry = result.objects.filter(category = data_id , user_id=user_detail , roll_no = roll)
        # print(result_entry)
        
        if result_entry.exists(): 
            print("Matching Found UPDATING !!")        
            result_entry = result_entry.update(s_name=student_name,roll_no=roll,f_name=father_name,m_name=mother_name,category=data_id, sgpa=sgpaS ,cgpa=c_result ,re_count=re_appear_count ,result_s = sub_result , user =user_detail)
            result_entry.save()

        else: 
            print("Matching not Found")        
            result_entry = result(s_name=student_name,roll_no=roll,f_name=father_name,m_name=mother_name,category=data_id, sgpa=sgpaS ,cgpa=c_result ,re_count=re_appear_count ,result_s = sub_result , user =user_detail)
            result_entry.save()
            
            # print("Hererererer")
        
        # print("saving funcitn call")
        count = 0
    except :
        count = 1
    return count
        
def image_rename(id , captcha_value):
    try :
        form = form_data.objects.get(id=id)

        # print("Here in porinting form_ :- ", form.captcha)
    
        old_file_path = os.path.join(media_path , f"{form.captcha}")
        
        new_file_name = f"{captcha_value}.png"  # Make sure to 
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
        print(new_file_path , old_file_path)
        os.rename(old_file_path, new_file_path)
        
        form.captcha = f"/images/{captcha_value}.png"
        form.save()
    except:
        pass



def image_rename2(id, captcha_value):
    try:
        form = form_data.objects.get(id=id)

        old_file_key = str(form.captcha).strip()
        new_file_key = f"media/Labeled/{captcha_value}.png"
        bucket_name = str(os.getenv('AWS_STORAGE_BUCKET_NAME')).strip()

        print(f"🔹 Bucket: {bucket_name}")
        print(f"🔹 Old File Key: {old_file_key}")
        print(f"🔹 New File Key: {new_file_key}")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_S3_REGION_NAME')
        )

        file_url = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{old_file_key}"
        print(f"📥 Downloading from URL: {file_url}")

        response = requests.get(file_url)
        
        if response.status_code != 200:
            print(f"❌ Error downloading file: {response.status_code} - {response.text}")
            return False  

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        print(f"✅ File downloaded successfully to {temp_file_path}")

        with open(temp_file_path, "rb") as data:
            s3_client.upload_fileobj(data, bucket_name, new_file_key)

        print(f"✅ File uploaded successfully with new name: {new_file_key}")

        s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)
        print(f"✅ Old file deleted: {old_file_key}")

        form.captcha = new_file_key
        form.save()
        print(f"✅ Database updated with new file path: {new_file_key}")

        os.remove(temp_file_path)
        print(f"✅ Temporary file deleted")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False