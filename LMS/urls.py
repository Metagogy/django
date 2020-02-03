from django.conf.urls import url,include

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()





from . import views
# from views import *

urlpatterns = [
# ============================ start of login ===============================
    
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^auth/', include('social_django.urls', namespace='social')),

# ============================ Courses and bundles =================================

    url(r'^courses/$', views.courses, name='courses'),
    url(r'^bundle/(\d+)/$', views.bundle, name='bundle'),
    url(r'^matchCase/$', views.courseSeacrh, name='courseSeacrh'),
    url(r'^course/(\d+)/$', views.course, name='course'),
   # url(r'^test/$', views.test, name='test'),
# ============================ cart =========================================
    
    url(r'^addToCart/(\w+)/(\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^deleteFromCart/(\d+)/$', views.cart_item_delete, name='cart_item_delete'),
    url(r'^cartCheckout/(\w+)/(\d+)/$', views.cart_checkout, name='cart_checkout'),
    url(r'^cartObjects/$', views.cartObjects, name='cartObjects'),

    url(r'^payment/$', views.payment, name='payment'),
    url(r'^registeredCourses/$', views.registeredCourses, name='registeredCourses'),

# ============================ Pretest  =========================================
 
    url(r'^pretest_landing/(\d+)/$', views.pretest_landing, name='pretest_landing'),
    url(r'^pretest_val/$', views.pretest_val, name='pretest_val'),
    
# ============================ Contents Display =========================================

    url(r'^contentsDisplay/(\w+)/(\d+)/$', views.contentsDisplay, name='contentsDisplay'),

# ============================ Topics and tests Display =========================================

   
    url(r'^Testvalidate/(\d+)$',views.Testvalidate,name='Testvalidate'),
    url(r'^topicAndTest/(\d+)/(\d+)/(\d+)/$', views.topicAndTest, name='topicAndTest'),
    # url(r'^page/$', views.TestAndTopic, name='page'),
    url(r'^TestOverview/(\d+)/(\d+)$', views.TestOverview, name='TestOverview'),
    url(r'^TimeFunctionality/$', views.test, name='test'),
  
# ============================ Assignments =========================================

    url(r'^Assignments/(\d+)/$', views.Assignments, name='Assignments'),
    url(r'^compiler/$', views.compiler, name='compiler'),
    url(r'^testcase/$', views.testcase, name='testcase'),
    url(r'^saveProblem/$', views.saveProblem, name='saveProblem'),
    url(r'^chapterOverview/(\d+)/(\d+)/$', views.chapterOverview, name='chapterOverview'),
    
# ============================ grouping =========================================
    url(r'^CourseGrouping/$', views.CourseGrouping, name='CourseGrouping'),
    url(r'^groupsDisplay/$', views.groupsDisplay, name='groupsDisplay'),
    

    url(r'^test_creation/$', views.test_creation, name='test_creation'),
    url(r'^test_ques/(?P<a>[0-9]+)/$', views.test_ques, name='test_ques'),
    url(r'^coursesList/$', views.coursesList, name='coursesList'),
    url(r'^chapt_topic_ajax/(?P<a>[0-9]+)/$', views.chapt_topic_ajax, name='chapt_topic_ajax'),
    


    
  
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
