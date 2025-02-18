from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from selenium.webdriver.support.ui import Select
from django.core.files.base import ContentFile
from selenium.webdriver.common.by import By
from django.http import JsonResponse
from django.contrib import messages
from selenium import webdriver
from .models import *
from .utils import *
import tempfile
import json
import os
from django.conf import settings
from django.contrib import messages


# Path to the media directory
media_path = settings.MEDIA_ROOT


driver = None

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")  # Run in headless mode for servers

    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    return webdriver.Chrome(options=options)

def home(request):
    global driver
    if driver:
        driver.quit()
        driver = None
    request.session.pop('current_state', None)
    
    return redirect('/profile/dashboard/')


@login_required(login_url='login')
def scraper_feed(request):
    if request.method == 'POST':
        param_start = request.POST['start_roll']
        param_end = request.POST['end_roll']
        param_semester = request.POST['semester']
        param_batch = request.POST['batch']
        param_branch = request.POST['branch']
        
        
        if not (len(param_start) == 11 and len(param_end) == 11):
            messages.error(request, "Invalid Roll Number")
            return redirect('feed')

        if param_start[:2] != param_end[:2]:
            messages.error(request, 'Make sure Both Roll Numbers are of the same Batch!!')
            return redirect('feed')
        
        if param_branch != branch_checker(param_start):
            messages.error(request, 'Make sure Roll Numbers are of the same Branch!!')
            return redirect('feed')

        if leet_checker(param_start):
            if int(param_start[:2]) - 1 != int(param_batch):
                messages.error(request, f'Make sure Leet {param_start[:2]} is of Batch {int(param_start[:2])-1}!!')
                return redirect('feed')
            
        if param_start[:2] != param_batch:
            messages.error(request , "Ensure Roll No and Batch are of same Category")
            return redirect('feed')
            
            
        param_end = int(param_end) + 1  # increment to include last roll number

        # Initialize the scraping session
        request.session['scraping_params'] = {
            'start_roll': param_start,
            'end_roll': param_end,
            'semester': param_semester,
            'current_roll': param_start,
            'branch' : param_branch,
            'batch' : param_batch,
            'form_filled': False 
        }
        
        return redirect('results', start_s=param_start, end_s=param_end, semester=param_semester , batch =param_batch , branch=param_branch)
    return render(request, 'scrap/scrap_feed.html')

driver = None



@login_required(login_url='login')
def run_scraper(request, start_s, end_s, semester , batch , branch):
    global driver
    
    # Get current roll number from session
    current_state = request.session.get('current_state', {})
    current_roll = current_state.get('roll_no', start_s)  # Use session roll no if exists, else use start_s
    
    if not driver:
        driver = setup_driver()
        driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")
    
    # Use current_roll instead of start_s
    roll_no_input = driver.find_element(By.ID, "txtRollNo")
    roll_no_input.clear()
    roll_no_input.send_keys(current_roll)  # Changed from start_s to current_roll
    
    semesters_list = ["First Semester", "Second Semester", "Third Semester", 
                      "Fourth Semester", "Fifth Semester", "Sixth Semester", 
                      "Seventh Semester", "Eighth Semester"]
    dropdown = Select(driver.find_element(By.ID, 'ddlSem'))
    dropdown.select_by_visible_text(semesters_list[int(semester)-1])
    
    # Get and save captcha
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx")
    
    captcha_element = driver.find_element(By.TAG_NAME, "img")
    screenshot = captcha_element.screenshot_as_png
    
    # Save to model using current_roll instead of start_s
    form_entry = form_data(
        roll_no=current_roll,  # Changed from start_s to current_roll
        semester=semester,
        user=request.user
    )
    captcha_file = ContentFile(screenshot, name=f"{current_roll}_{semester}.png")  # Changed from start_s to current_roll
    form_entry.captcha.save(f"{current_roll}_{semester}.png", captcha_file, save=False)
    form_entry.save()
    image_id = form_entry.id
    
    data = form_data.objects.filter(id=image_id).values('captcha')
    image_url = data[0]['captcha']
    
    # print(current_roll)
    # Update session state

    # print(user.profile.image.path)

    request.session['current_state'] = {
        'roll_no': current_roll,  # Changed from start_s to current_roll
        'end_roll': end_s,
        'semester': semester,
        'batch' : batch,
        'branch' : branch,
        'form_entry_id': form_entry.id
    }
    
    driver.switch_to.window(driver.window_handles[0])
    
    return render(request, 'scrap/result_scrap.html', {
        'form_data': form_entry,
        'current_roll': current_roll,  # Changed from start_s to 
        'image_url': image_url
    })



@login_required(login_url='login')
@require_POST
def submit_captcha(request):
    """Separate view to handle captcha submission"""
    global driver
    user = request.user
    if not driver:
        return JsonResponse({'status': 'error', 'message': 'Session expired'})
    
    try:
        captcha_value =request.POST.get('captcha_value')
        captcha_value = captcha_value.upper()
        current_state = request.session.get('current_state', {})
        
        driver.switch_to.window(driver.window_handles[0])

        captcha_input = driver.find_element(By.ID, "txtCaptcha")
        captcha_input.clear()
        captcha_input.send_keys(captcha_value)
        
        
        submit_button = driver.find_element(By.ID, "btnResult")
        submit_button.click()
        
    
        # print("================================================")
        # print(len(driver.window_handles))
        # print(driver.title)
        
        # print("-----------------------------------------------")
        driver.switch_to.window(driver.window_handles[1])
        # print(driver.title)
        # print("-----------------------------------------------")
        """  
        # def subject_parse(soup):
        #     subject_code= []
        #     subject_name = []
        #     credit = []
        #     theory = []
        #     sessional = []
        #     practicle = []
        #     pass_s = []

        #     for i in range(16 , 150 , 8):
        #         try:
        #             table = "".join(soup.select('tr')[i].select('td')[2].text.split())
        #             subject_code.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[3].text.split())
        #             subject_name.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[4].text.split())
        #             credit.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[14].text.split())
        #             theory.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[16].text.split())
        #             sessional.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[18].text.split())
        #             practicle.append(table)
        #             # print("------------------------------------------------")
        #             table = " ".join(soup.select('tr')[i].select('td')[19].text.split())
        #             pass_s.append(table)
        #         except: pass
        #     theory = [x if x != "NA" and x != "" else "0" for x in theory]
        #     sessional = [x if x != "NA" and x != "" else "0" for x in sessional]
        #     practicle = [x if x != "NA" and x != "" else "0" for x in practicle]
        #     total_marks = list(map(lambda x, y , z: int(x) + int(y) +int(z), theory, sessional , practicle))
            

        #     result_s ={
        #     "subject_code": subject_code,
        #     "subject_name": subject_name,
        #     "credit": credit,
        #     "theory": theory,
        #     "sessional": sessional,
        #     "practicle": practicle,
        #     "total_marks": total_marks,
        #     "pass_s": pass_s
        #     }

        #     result_s = json.dumps(result_s)
        #     result_s = json.loads(result_s)
        #     subjects = {}
            
        #     for i in range(len(result_s["subject_code"])):
        #         subject_code = result_s["subject_code"][i]
        #         subjects[subject_code] = {
        #             "Subject Name": result_s["subject_name"][i],
        #             "Credits": result_s["credit"][i],
        #             "Theory": int(result_s["theory"][i]) if result_s["theory"][i] else 0,
        #             "Sessional": int(result_s["sessional"][i]),
        #             "Practical": int(result_s["practicle"][i]) if result_s["practicle"][i] else 0,
        #             "Total Marks": result_s["total_marks"][i],
        #             "Grade": result_s["pass_s"][i]
        #         }
                
        #     print(subjects)
        #     return json.dumps(subjects)

        # def data_save(current_state, page_s , user):
        #     count = ''
        #     try:
        #         batch = current_state['batch']
        #         branch = current_state['branch']
        #         roll_no = current_state['roll_no']
        #         semester_cat = current_state['semester']
                
        #         data_id = "_".join([branch ,batch , semester_cat]) 
                
        #         soup = BeautifulSoup(page_s, 'html.parser')
                
        #         student_name = soup.find(id ="lblname").text
                
        #         roll = soup.find(id = "lblRollNo").text
                
        #         mother_name = soup.find(id = "lblMotherName").text

        #         father_name = soup.find(id = "lblFatherName").text
                
        #         sgpaS = soup.find(id = "lblResult").text
        #         re_appear_count = ''

        #         try :
        #             if isinstance(float(sgpaS) , float):
        #                 print("True integer")
        #                 sgpa = float(sgpaS)
        #                 re_appear_count = 0
        #                 print(re_appear_count , sgpaS)
        #         except:
        #             sgpaS = sgpaS.split()
        #             re_appear_count = len(sgpaS)
        #             print(re_appear_count , sgpaS)
        #             print("Not an integer")
                            
        #         c_result = soup.find(id = "lblCgpaResult").text
                
        #         print("Here before process_Sub_result")
                
        #         #EVERYTHING FINE TILL HERE
        #         sub_result =  json.loads(subject_parse(soup))
        #         print("Here after process_sgpa")
                
        #         print("here " , student_name,roll,father_name,mother_name,data_id,sgpaS,c_result ,re_appear_count , sub_result)
        #         print("Here after process_sgpa")
                
        #         result_entry = result.objects.filter(category = data_id , user_id=request.user , roll_no = roll)
        #         print(result_entry)
                
        #         if result_entry.exists(): 
        #             print("Matching Found UPDATING !!")        
        #             result_entry = result(s_name=student_name,roll_no=roll,f_name=father_name,m_name=mother_name,category=data_id, sgpa=sgpaS ,cgpa=c_result ,re_count=re_appear_count ,result_s = sub_result , user =user)
        #             result_entry.save()

        #         else: 
        #             print("Matching not Found")        
        #             result_entry = result(s_name=student_name,roll_no=roll,f_name=father_name,m_name=mother_name,category=data_id, sgpa=sgpaS ,cgpa=c_result ,re_count=re_appear_count ,result_s = sub_result , user =user)
        #             result_entry.save()
        #             print("Hererererer")
                
        #         print("saving funcitn call")
        #         count = 0
        #     except :
        #         count = 1
        #     return count
                
        # def image_rename(id , captcha_value):
        #     try :
        #         form = form_data.objects.get(id=id)
            
        #         old_file_path = os.path.join(media_path , f"{form.captcha}")
                
        #         new_file_name = f"{captcha_value}.png"  # Make sure to 
        #         new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
        #         os.rename(old_file_path, new_file_path)
                
        #         form.captcha = f"images/{captcha_value}.png"
        #         form.save()
        #     except:
        #         print("In image_rename")"""
                       
        if len(driver.window_handles)==3:
            driver.switch_to.window(driver.window_handles[2])
            
            data_save(current_state , driver.page_source , user)   
            image_rename2(current_state['form_entry_id'], captcha_value)
         
            driver.close()       
                   
        # Process result page he
        # Update roll number
        
        next_roll = str(int(current_state['roll_no']) + 1)
        # print("Next New Roll No : ", next_roll)
        
        if int(next_roll) >= int(current_state['end_roll']):
            driver.quit()
            driver = None
            return JsonResponse({'status': 'completed'})
        
        # Update session with new roll number
        current_state['roll_no'] = next_roll
        request.session['current_state'] = current_state
        request.session.modified = True  # Force session update
        
        # Close extra windows and prepare for next roll
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        

        # Return success with next roll number
        return JsonResponse({
            'status': 'success', 
            'next_roll': next_roll,
            'batch' : current_state['batch'],
            'redirect_url': f'/profile/scrap/results/{next_roll}/{current_state["end_roll"]}/{current_state["semester"]}/{current_state['batch']}/{current_state['branch']}'
        })
        
        
    except Exception as e:
        # print("InLast exception")
        return JsonResponse({'status': 'error', 'message': str(e)})



def json_trial(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll')
        json_data_str = request.POST.get('json_data')  # Fix the name to match the form

        try:
            # Parse JSON data
            json_data = json.loads(json_data_str)
            
            # Save to the database
            trail_json_instance = trail_json.objects.create(
                name=name,
                roll_no=roll_no,
                result=json_data
            )

            print(name, roll_no, json_data)
            return JsonResponse({'message': 'Data saved successfully!', 'id': trail_json_instance.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return render(request, "scrap/trail_json.html")

def checkhtml(request):
    return render(request , "scrap/temp_database.html") 