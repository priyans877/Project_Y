from django.shortcuts import render, HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

# Create your views here.

def temp_fi(request):
    urls = "https://images.pexels.com/photos/4005448/pexels-photo-4005448.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    return render(request , 'scrap/result_scrap.html' , {"image":f"{urls}"})



def run_scraper(driver):
    # Getting Url 
    driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")
    
    # finding RollNo Field
    roll_no_object = driver.find_element(By.ID, "txtRollNo")

    roll_no_object.send_keys("21011018024")
    dropdown = driver.find_element(By.ID, 'ddlSem')
    select = Select(dropdown)
    select.select_by_visible_text('First Semester')

    return "<h1>Scraper ran successfully</h1>"

def scraper_feed(request):
    if request.method == 'POST':
        start_roll = request.POST['start_roll']
        end_roll = request.POST['end_roll']
        semester = request.POST['semester']
        
        print(start_roll , end_roll , semester)
    return render(request , 'scrap/scrap_feed.html')


def home(request):
    return render(request , 'scrap/base.html')
