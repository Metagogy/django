from django.conf.urls import url,include

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^open/(\d+)/$', views.open, name='open'),
    url(r'^questionUpload/(\d+)/$', views.questionUpload, name='questionUpload'),
    url(r'^quesAnswers/(\d+)/$', views.quesAnswers, name='quesAnswers'),
    url(r'^editanswer/(\d+)/$', views.editanswer, name='editanswer'),
    url(r'^deleteAnswer/(\d+)/$', views.deleteAnswer, name='deleteAnswer'),
    url(r'^deleteRedirect/(\d+)/$', views.deleteRedirect, name='deleteRedirect'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^dashboard/$', views.Dashboard, name='dashboard'),
    url(r'^searchQuestions/$', views.searchQuestions, name='searchQuestions'),
    url(r'^closeQues/(\d+)/$', views.closeQues, name='closeQues'),
    url(r'^closed/(\d+)/$', views.closed, name='closed'),
    url(r'^unClosedQues/(\d+)/$', views.unClosedQues, name='unClosedQues'),
    url(r'^globalize/(\d+)/$', views.globalize, name='globalize'),
    url(r'^globalized/(\d+)/$', views.globalized, name='globalized'),
    url(r'^keywordSearch/$', views.keywordSearch, name='keywordSearch'),
    url(r'^editQuestion/(\d+)/$', views.editQuestion, name='editQuestion'),
    
    url(r'^A2AQuestionUpload/(\d+)/(\d+)/$', views.A2AQuestionUpload, name='A2AQuestionUpload'),
    url(r'^ToBeAnswered/(\d+)/$', views.ToBeAnswered, name='ToBeAnswered'),
    url(r'^A2AquesAnswers/(\d+)/$', views.A2AquesAnswers, name='A2AquesAnswers'),
    url(r'^A2Averify/$', views.A2Averify, name='A2Averify'),
    url(r'^A2AoutgoingAnswers/(\d+)/$', views.A2AoutgoingAnswers, name='A2AoutgoingAnswers'),
    

]
