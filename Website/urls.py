
from django.conf.urls import url,include

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin







from . import views
# from views import *

urlpatterns = [

url(r'^contact/$', views.contact, name='contact'),
url(r'^about/$', views.about, name='about'),
url(r'^techArticles/$', views.tech, name='tech'),
url(r'^internships/$', views.internships, name='internships'),
url(r'^events/$', views.events, name='events'),
]