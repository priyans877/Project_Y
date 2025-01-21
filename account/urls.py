from django.contrib import admin
from django.urls import path
import views 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page , name="login"),
    path('logout/', views.logout_page , name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)