
from django.conf.urls import include, url
from django.contrib import admin
#from django.views.generic.base import TemplateView
# from . import views
from django.contrib import auth

from django.contrib.auth import views as auth_views
from LMS.views import *
from Users.views import *


from Website.views import *

urlpatterns = [
 #path(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url('',include('social_django.urls', namespace='social')),
    
    
     
    url(r'^', include('LMS.urls')),
    url(r'^', include('Support.urls')),
    
    url(r'^', include('Users.urls')),
   
    url(r'^', include('Website.urls')),

    
    #path('polls/', include('django.contrib.auth.urls')),
    #path('edx_auth/', views.edx_auth.as_view(), name='edx_auth'),
]


from django_project import settings

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
