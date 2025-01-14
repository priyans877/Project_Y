

from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('scrap' , views.home , name='home'),
    path('scrap/feed' , views.scraper_feed , name='feed'),
    path('scrap/results' , views.temp_fi, name='results'),
]