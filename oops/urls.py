from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("oops/", views.under_dev, name="oops")
]