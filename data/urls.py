from django.contrib import admin
from django.urls import path
import data.views as views



urlpatterns = [
    path('', views.get_data , name="get_data"),

]
