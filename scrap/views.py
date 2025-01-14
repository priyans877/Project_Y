from django.shortcuts import render, HttpResponse , redirect
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
    urls = "https://jcboseustymca.co.in/Handler/GenerateCaptchaImage.ashx"
    return render(request , 'scrap/result_scrap.html' , {"image":f"{urls}"})


def run_scraper(request, start_s, end_s, semester):
    # Assuming start_s and end_s are valid integers
    start = int(start_s)
    end = int(end_s)
    
    # Setting up the driver (replace this with actual driver setup)
    driver = setup_driver()  # Placeholder for actual driver setup
    
    # Call the scraping function
    result_message = run_scraper_logic(driver, start, end, semester)
    
    # Return a response
    return HttpResponse(result_message)

def run_scraper_logic(driver, start, end, semester):
    # Scraping logic (as in your original run_scraper function)
    driver.get("https://jcboseustymca.co.in/Forms/Student/ResultStudents.aspx")

    roll_no_object = driver.find_element(By.ID, "txtRollNo")
    dropdown = driver.find_element(By.ID, 'ddlSem')
    
    for i in range(start, end):
        roll_no_object.clear()  # Clear the input field before sending keys
        roll_no_object.send_keys(f"210110180{i}")
        select = Select(dropdown)
        select.select_by_visible_text(semester)
        driver.find_element(By.ID, "bbtnResult").click()
        driver.switch_to.window(driver.window_handles[1])
        # You may want to add logic to handle the results or close the tab
    
    return "<h1>Scraper ran successfully</h1>"


def home(request):
    return render(request , 'scrap/base.html')
