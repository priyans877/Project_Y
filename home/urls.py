from django.contrib import admin
from django.urls import path
from home import views
from django.views.generic import RedirectView

urlpatterns = [
    path('public/home/', views.home_public , name="home"),
    path('public/resp/', views.resp , name="resp"),
    path('profile/dashboard/', views.dashboard , name="home_dash"),
    path('oops/', views.under_dev , name="under_dev"),
    path('',RedirectView.as_view(url='/public/home/' ,permanent=True) , name="home" )
]
