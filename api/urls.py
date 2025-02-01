from home.views import *
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('index/', resp),
    path('chart_p/', get_chart),
]
