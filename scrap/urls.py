
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('scrap/', views.home, name='home'),
    path('scrap/feed/', views.scraper_feed, name='feed'),
    path('scrap/results/<slug:start_s>/<slug:end_s>/<slug:semester>/<slug:batch>/<slug:branch>', views.run_scraper, name='results'),
    path('scrap/submit-captcha/', views.submit_captcha, name='submit_captcha'),# New URL for captcha submission
    path('' , views.checkhtml , name = "Json_trial"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)