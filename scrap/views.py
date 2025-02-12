from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from selenium.webdriver.support.ui import Select
from django.core.files.base import ContentFile
from selenium.webdriver.common.by import By
from django.http import JsonResponse
from django.contrib import messages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import *
from .utils import *
import tempfile
import json
import os
from django.conf import settings

media_path = settings.MEDIA_ROOT

driver = None

def setup_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/google-chrome"
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
            driver = None
        raise Exception(f"Failed to initialize driver: {str(e)}")

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
        param_end = int(param_end)+1
        request.session['scraping_params'] = {
            'start_roll': param_start,
            'end_roll': param_end,
            'semester': param_semester,
            'current_roll': param_start,
            'branch': param_branch,
            'batch': param_batch,
            'form_filled': False
        }
        return redirect('results', start_s=param_start, end_s=param_end, semester=param_semester, batch=param_batch, branch=param_branch)
    return render(request, 'scrap/scrap_feed.html')

@login_required(login_url='login')
def run_scraper(request, start_s, end_s, semester, batch, branch):
    global driver
    try:
        current_state = request.session.get('current_state', {})
        current_roll = current_state.get('roll_no', start_s)
        if not driver:
            driver = setup_driver()
            driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")
        wait = WebDriverWait(driver, 10)
        roll_no_input = wait.until(EC.presence_of_element_located((By.ID, "txtRollNo")))
        roll_no_input.clear()
        roll_no_input.send_keys(current_roll)
        semesters_list = ["First Semester", "Second Semester", "Third Semester", "Fourth Semester", "Fifth Semester", "Sixth Semester", "Seventh Semester", "Eighth Semester"]
        dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ddlSem')))
        dropdown = Select(dropdown)
        dropdown.select_by_visible_text(semesters_list[int(semester)-1])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx")
        captcha_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        screenshot = captcha_element.screenshot_as_png
        form_entry = form_data(roll_no=current_roll, semester=semester, user=request.user)
        captcha_file = ContentFile(screenshot, name=f"{current_roll}_{semester}.png")
        form_entry.captcha.save(f"{current_roll}_{semester}.png", captcha_file, save=False)
        form_entry.save()
        data = form_data.objects.filter(id=form_entry.id).values('captcha')
        image_url = data[0]['captcha']
        request.session['current_state'] = {
            'roll_no': current_roll,
            'end_roll': end_s,
            'semester': semester,
            'batch': batch,
            'branch': branch,
            'form_entry_id': form_entry.id
        }
        driver.switch_to.window(driver.window_handles[0])
        return render(request, 'scrap/result_scrap.html', {
            'form_data': form_entry,
            'current_roll': current_roll,
            'image_url': image_url
        })
    except Exception as e:
        if driver:
            driver.quit()
            driver = None
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='login')
@require_POST
def submit_captcha(request):
    global driver
    try:
        if not driver:
            return JsonResponse({
                'status': 'error', 
                'message': 'Browser session expired. Please start over from the beginning.'
            })
        
        captcha_value = request.POST.get('captcha_value', '').upper()
        current_state = request.session.get('current_state', {})
        wait = WebDriverWait(driver, 10)
        driver.switch_to.window(driver.window_handles[0])
        captcha_input = wait.until(EC.presence_of_element_located((By.ID, "txtCaptcha")))
        captcha_input.clear()
        captcha_input.send_keys(captcha_value)
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnResult")))
        submit_button.click()
        if len(driver.window_handles) == 3:
            driver.switch_to.window(driver.window_handles[2])
            data_save(current_state, driver.page_source, request.user)
            image_rename2(current_state['form_entry_id'], captcha_value)
            driver.close()
        next_roll = str(int(current_state['roll_no']) + 1)
        
        if int(next_roll) >= int(current_state['end_roll']):
            driver.quit()
            driver = None
            return JsonResponse({'status': 'completed'})
            
        current_state['roll_no'] = next_roll
        request.session['current_state'] = current_state
        request.session.modified = True
        
        driver.switch_to.window(driver.window_handles[1])
        a = driver.title
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        b = driver.title
        return JsonResponse({
            'status': 'success',
            'message': f"driver name {a ,b }",
            'next_roll': next_roll,
            'batch': current_state['batch'],
            'redirect_url': f'/profile/scrap/results/{next_roll}/{current_state["end_roll"]}/{current_state["semester"]}/{current_state["batch"]}/{current_state["branch"]}'
        })
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
            driver = None
        return JsonResponse({'status': 'error', 'message': str(e)})

def json_trial(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll')
        json_data_str = request.POST.get('json_data')
        try:
            json_data = json.loads(json_data_str)
            trail_json_instance = trail_json.objects.create(name=name, roll_no=roll_no, result=json_data)
            print(name, roll_no, json_data)
            return JsonResponse({'message': 'Data saved successfully!', 'id': trail_json_instance.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return render(request, "scrap/trail_json.html")

def checkhtml(request):
    return render(request, "scrap/temp_database.html")
