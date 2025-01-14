from django.shortcuts import render, HttpResponse , redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from .models import form_data
from io import BytesIO
from django.core.files.base import ContentFile



# Create your views here.
def temp_fi(request):
    urls = "https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx"
    return render(request , 'scrap/result_scrap.html' , {"image":f"{urls}"})



def run_scraper(request ,start_s , end_s , semester):
    # Getting Url 

    def setup_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)
    
    def image_loader(driver, roll, semester):
        # Navigate to the CAPTCHA URL
        driver.get("https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx")

        captcha_element = driver.find_element(By.TAG_NAME, "img")

        screenshot = captcha_element.screenshot_as_png
        captcha_file = ContentFile(screenshot, name=f"{roll}_{semester}.png")
        # Create and save the form_data instance
        form_entry = form_data(
            roll_no=roll,
            semester=semester
        )
        print("In Loader")
        form_entry.captcha.save(f"{roll}_{semester}.png", captcha_file, save=False)
        form_entry.save()
        return form_entry
        
    
    driver = setup_driver()
    
    driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")
    
    for i in range(int(start_s) , int(end_s)+1):
        # starting driver url
        semesters_list = ["First Semester","Second Semester","Third Semester","Fourth Semester","Fifth Semester","Sixth Semester","Seventh Semester","Eighth Semester"]
        semester = semesters_list[int(semester)-1]
        
        # Defining Rollno Field & send keys 
        driver.find_element(By.ID, "txtRollNo").send_keys(f"{i}")
        # Defining Semester Dropdown & selecting the semester
        select = Select(driver.find_element(By.ID, 'ddlSem'))
        select.select_by_visible_text(semester)
        
        # Submitting the form
        image_loader(driver, f"{i}", semester)
        
        data = form_data.objects.all()
        print(data)
        
        
        
        driver.find_element(By.ID, "btnResult").click()
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.ID, "txtRollNo").clear()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        
    # finding RollNo Field
    '''roll_no_object = driver.find_element(By.ID, "txtRollNo")
    dropdown = driver.find_element(By.ID, 'ddlSem')
    
    for i in range(start , end):
        roll_no_object.send_keys(f"210110180{i}")
        select = Select(dropdown)
        select.select_by_visible_text(semester)
        # Submitting the form
        driver.find_element(By.ID, "bbtnResult").click()
        # Getting the result
        driver.switch_to.window(driver.window_handles[1])
        
        # Clearing the roll_no field
    print("Here run")'''
    
    '''roll_no_object.send_keys("21011018024")
    
    # select = Select(dropdown)
    # select.select_by_visible_text('First Semester')'''

    return render(request , 'scrap/result_scrap.html')

def scraper_feed(request):
    if request.method == 'POST':
        print("Hii")
        param_start= request.POST['start_roll']
        param_end = request.POST['end_roll']
        param_semester = request.POST['semester']
        
        """# Setting up the driver
        print(param_start)
        print(param_end)
        print(param_semester)
        #run_scraper(driver ,start_roll , end_roll , semester)
        print("Hii")"""
        return redirect(f'/scrap/results/{param_start}/{param_end}/{param_semester}/')
  
    return render(request , 'scrap/scrap_feed.html')


def home(request):
    return render(request , 'scrap/base.html')
