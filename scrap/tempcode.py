
            count = driver.window_handles
            print(f"get the number of headless : {len(count)}")
            print("---------------------------------------------")
            print("Driver title at 0 index " , driver.title)
            
            driver.switch_to.window(driver.window_handles[1])
            
            print("Driver title  at index 1 : ",driver.title)
            
            driver.switch_to.window(driver.window_handles[2])
            print("Got result Page Success Fully")
            
            file_path = "tempfile/temp_code.html"
            with open(file_path, 'a') as file:
                file.write(driver.page_source)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .models import form_data
import json

def Setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def home(request):
    return render(request, 'scrap/base.html')

def scraper_feed(request):
    if request.method == 'POST':
        param_start = request.POST['start_roll']
        param_end = request.POST['end_roll']
        param_semester = request.POST['semester']
        
        # Store parameters in session
        request.session['scraping_params'] = {
            'start_roll': param_start,
            'end_roll': param_end,
            'semester': param_semester,
            'current_roll': param_start  # Track current roll number
        }
        
        return redirect('results', start_s=param_start, end_s=param_end, semester=param_semester)
    return render(request, 'scrap/scrap_feed.html')

def image_loader(driver, roll, semester):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx")
    
    captcha_element = driver.find_element(By.TAG_NAME, "img")
    screenshot = captcha_element.screenshot_as_png
    
    # Save captcha image
    captcha_file = ContentFile(screenshot, name=f"{roll}_{semester}.png")
    form_entry = form_data(
        roll_no=roll,
        semester=semester
    )
    form_entry.captcha.save(f"{roll}_{semester}.png", captcha_file, save=False)
    form_entry.save()
    
    driver.close()  # Close captcha tab
    driver.switch_to.window(driver.window_handles[0])
    return driver , form_entry.id

def run_scraper(request, start_s, end_s, semester):
    # Get or initialize session data
    scraping_params = request.session.get('scraping_params', {})
    current_roll = int(scraping_params.get('current_roll', start_s))
    driver = Setup_driver()
    
    
    # For GET request or after POST processing
    driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")  # Replace with actual URL
    driver , image_id = image_loader(driver, str(current_roll), semester)
    data = form_data.objects.filter(id=image_id).values('captcha')
    image_url = data[0]['captcha']
    messages.success(request, f"Please enter captcha for roll number {current_roll}")
    
    if request.method == 'POST':
        captcha_value = request.POST.get('Captcha_value')
        
        try:
            # Navigate to result page
            print(len(driver.window_handles))  # Replace with actual URL
            print(driver.title)
            # Fill form
            roll_no_input = driver.find_element(By.ID, "txtRollNo")
            roll_no_input.clear()
            roll_no_input.send_keys(str(current_roll))
            
            # Select semester
            semesters_list = ["First Semester", "Second Semester", "Third Semester", 
                            "Fourth Semester", "Fifth Semester", "Sixth Semester", 
                            "Seventh Semester", "Eighth Semester"]
            dropdown = Select(driver.find_element(By.ID, 'ddlSem'))
            dropdown.select_by_visible_text(semesters_list[int(semester)-1])
            
            # Enter captcha and submit
            captcha_input = driver.find_element(By.ID, "txtCaptcha")  # Update with actual ID
            captcha_input.send_keys(captcha_value)
            submit_button = driver.find_element(By.ID, "btnResult")  # Update with actual ID
            submit_button.click()
            print(driver.find_element(By.ID , "lblMessage").text)
            print(driver.title)
            print(len(driver.window_handles))
            
            # Process result page here
            # ... Add your result processing logic ...
            
            # Update current roll for next iteration
            current_roll += 1
            scraping_params['current_roll'] = current_roll
            request.session['scraping_params'] = scraping_params
            
            if current_roll >= int(end_s):
                messages.success(request, "Scraping completed!")
                return redirect('home')
            
        finally:
            driver.quit()
    

  
    
    return render(request, 'scrap/result_scrap.html', {
        'current_roll': current_roll,
        'image_id': image_id ,
        'image_url' :image_url
    })
        