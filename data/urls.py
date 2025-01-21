from django.contrib import admin
from django.urls import path
import data.views as views



urlpatterns = [
    path('', views.get_data , name="get_data"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page , name="login"),
    path('logout/', views.logout_page , name="logout"),
]
