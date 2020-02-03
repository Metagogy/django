from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^verifyAccount/$' , views.verifyAccount , name = 'verifyAccount' ),
    url(r'^auth/$', views.login_auth, name='edx_auth'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^changePassword/$', views.changePassword, name='changePassword'),
    url(r'^profile/$', views.profile, name='profile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)