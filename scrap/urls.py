
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('scrap/', views.home, name='home'),
    path('scrap/feed/', views.scraper_feed, name='feed'),
    path('scrap/results/<slug:start_s>/<slug:end_s>/<slug:semester>/', views.run_scraper, name='results'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)