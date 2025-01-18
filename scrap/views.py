from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .models import form_data , trail_json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import os
from django.conf import settings

# Path to the media directory
media_path = settings.MEDIA_ROOT

driver = None

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def home(request):
    global driver
    if driver:
        driver.quit()
        driver = None
    return render(request, 'scrap/base.html')

def scraper_feed(request):
    if request.method == 'POST':
        param_start = request.POST['start_roll']
        param_end = request.POST['end_roll']
        param_semester = request.POST['semester']
        param_batch = request.POST['batch']
        param_branch = request.POST['branch']
   
        
        # Initialize the scraping session
        request.session['scraping_params'] = {
            'start_roll': param_start,
            'end_roll': param_end,
            'semester': param_semester,
            'current_roll': param_start,
            'branch' : param_branch,
            'batch' : param_batch,
            'form_filled': False  # Track if we've filled the form
        }
        
        return redirect('results', start_s=param_start, end_s=param_end, semester=param_semester , batch =param_batch , branch=param_branch)
    return render(request, 'scrap/scrap_feed.html')

driver = None

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
        semester=semester
    )
    captcha_file = ContentFile(screenshot, name=f"{current_roll}_{semester}.png")  # Changed from start_s to current_roll
    form_entry.captcha.save(f"{current_roll}_{semester}.png", captcha_file, save=False)
    form_entry.save()
    image_id = form_entry.id
    
    data = form_data.objects.filter(id=image_id).values('captcha')
    image_url = data[0]['captcha']
    
    print(current_roll)
    # Update session state
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
        'current_roll': current_roll,  # Changed from start_s to current_roll
        'image_url': image_url
    })



 


@require_POST
def submit_captcha(request):
    """Separate view to handle captcha submission"""
    global driver
    
    if not driver:
        return JsonResponse({'status': 'error', 'message': 'Session expired'})
    
    try:
        captcha_value = request.POST.get('captcha_value')
        current_state = request.session.get('current_state', {})
        
        # Switch to main window and submit captcha
        driver.switch_to.window(driver.window_handles[0])
        
        # Enter captcha
        captcha_input = driver.find_element(By.ID, "txtCaptcha")
        captcha_input.clear()
        captcha_input.send_keys(captcha_value)
        
        
        submit_button = driver.find_element(By.ID, "btnResult")
        submit_button.click()
        
    
        print("================================================")
        print(len(driver.window_handles))
        print(driver.title)
        
        print("-----------------------------------------------")
        driver.switch_to.window(driver.window_handles[1])
        print(driver.title)
        print("-----------------------------------------------")
        
        
        def data_save(current_state, page_s):
            batch = current_state['batch']
            branch = current_state['branch']
            roll_no = current_state['roll_no']
            
            print(f"Data saved for Roll No: {roll_no}, Batch: {batch}, Branch: {branch}")
        
        def image_rename(id , captcha_value):
            form = form_data.objects.get(id=id)
            
            old_file_path = os.path.join(media_path , f"{form.captcha}")
            
            new_file_name = f"{captcha_value}.png"  # Make sure to 
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
            os.rename(old_file_path, new_file_path)
            
            form.captcha = f"images/{captcha_value}.png"
            form.save()
    
                        
            
        if len(driver.window_handles)==3:
            driver.switch_to.window(driver.window_handles[2])
            print(driver.title)
            
            data_save(current_state , driver.page_source)
            image_rename(current_state['form_entry_id'], captcha_value)
            
            print("================================================")
            
            driver.close()       
                   
        # Process result page he
        # Update roll number
        
        next_roll = str(int(current_state['roll_no']) + 1)
        print("Next New Roll No : ", next_roll)
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
            'redirect_url': f'/scrap/results/{next_roll}/{current_state["end_roll"]}/{current_state["semester"]}/'
        })
        
    except Exception as e:
        print("InLast exception")
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