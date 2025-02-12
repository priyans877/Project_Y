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
import atexit


media_path = settings.MEDIA_ROOT


class WebDriverManager:
    def __init__(self):
        self._driver = None
        atexit.register(self.cleanup)
    
    def get_driver(self):
        if not self._driver:
            self._driver = self.setup_driver()
        return self._driver
    
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.binary_location = "/usr/bin/google-chrome"
        temp_user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_user_data_dir}")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        return driver
    
    def quit_driver(self):
        if self._driver:
            try:
                self._driver.quit()
            except:
                pass
            finally:
                self._driver = None
    
    def cleanup(self):
        self.quit_driver()
driver_manager = WebDriverManager()

def home(request):
    driver_manager.quit_driver()
    request.session.pop('current_state', None)
    return redirect('/profile/dashboard/')

@login_required(login_url='login')
def run_scraper(request, start_s, end_s, semester, batch, branch):
    try:
   
        current_state = request.session.get('current_state', {})
        current_roll = current_state.get('roll_no', start_s)
        driver = driver_manager.get_driver()
        
        if driver.current_url != "https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx":
            driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")
        
        #waiting for elements to be present
        wait = WebDriverWait(driver, 10)
        roll_no_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtRollNo"))
        )
        roll_no_input.clear()
        roll_no_input.send_keys(current_roll)
        
        semesters_list = ["First Semester", "Second Semester", "Third Semester", 
                         "Fourth Semester", "Fifth Semester", "Sixth Semester", 
                         "Seventh Semester", "Eighth Semester"]
        
        dropdown = wait.until(
            EC.presence_of_element_located((By.ID, 'ddlSem'))
        )
        dropdown = Select(dropdown)
        dropdown.select_by_visible_text(semesters_list[int(semester)-1])
  
        if len(driver.window_handles) < 2:
            driver.execute_script("window.open('');")
        
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx")
        
        captcha_element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        screenshot = captcha_element.screenshot_as_png
        
        #save to model
        form_entry = form_data(
            roll_no=current_roll,
            semester=semester,
            user=request.user
        )
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
        driver_manager.quit_driver()
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='login')
@require_POST
def submit_captcha(request):
    try:
        driver = driver_manager.get_driver()
        if not driver:
            return JsonResponse({'status': 'error', 'message': 'Session expired'})
        
        captcha_value = request.POST.get('captcha_value', '').upper()
        current_state = request.session.get('current_state', {})
        
        wait = WebDriverWait(driver, 10)
        
        driver.switch_to.window(driver.window_handles[0])
        
        captcha_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtCaptcha"))
        )
        captcha_input.clear()
        captcha_input.send_keys(captcha_value)
        
        submit_button = wait.until(
            EC.element_to_be_clickable((By.ID, "btnResult"))
        )
        submit_button.click()

        if len(driver.window_handles) == 3:
            driver.switch_to.window(driver.window_handles[2])
            data_save(current_state, driver.page_source, request.user)
            image_rename2(current_state['form_entry_id'], captcha_value)
            driver.close()

        next_roll = str(int(current_state['roll_no']) + 1)
        
        if int(next_roll) >= int(current_state['end_roll']):
            driver_manager.quit_driver()
            return JsonResponse({'status': 'completed'})
        
        current_state['roll_no'] = next_roll
        request.session['current_state'] = current_state
        request.session.modified = True
        

        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        return JsonResponse({
            'status': 'success',
            'next_roll': next_roll,
            'batch': current_state['batch'],
            'redirect_url': f'/profile/scrap/results/{next_roll}/{current_state["end_roll"]}/{current_state["semester"]}/{current_state["batch"]}/{current_state["branch"]}'
        })
        
    except Exception as e:
        driver_manager.quit_driver()
        return JsonResponse({'status': 'error', 'message': str(e)})
