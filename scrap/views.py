from django.shortcuts import render, HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)
# Create your views here.

def run_scraper():
    driver = setup_driver()
    driver.get('https://www.google.com')
    print(driver.title)
    driver.quit()
    return "<h1>Scraper ran successfully</h1>"

def home(request):
    a = run_scraper()
    return HttpResponse("<h1> Hello World {a}</h1>")
