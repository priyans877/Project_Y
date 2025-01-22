from django.contrib import admin
from django.urls import path
import data.views as views



urlpatterns = [
    path('', views.get_data , name="get_data"),
    path('download/<slug:fileName>', views.download_excel , name="d_data"),
    path('file/<slug:file_name>', views.file_download , name="file_download"),

]
