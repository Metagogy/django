import os, sys
import urllib2
import time,urllib2,urllib
import json
import ast
import random
import string 
from itertools import chain
from random import randrange, choice, randint 
from collections import OrderedDict 
from urllib2 import Request
from datetime import datetime,timedelta

# import tensorflow as tf
# import gym
# import ShAl
# import numpy as np
# from AandC import *

from django.shortcuts import render, redirect,get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned,ValidationError
from django.contrib.auth import update_session_auth_hash,hashers
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django_project.settings import STATIC_ROOT, MEDIA_ROOT,EMAIL_HOST_USER
from django.views.decorators.csrf import csrf_exempt
from  online_users.models import OnlineUserActivity

from LMS.models import *
from .forms import UploadFileForm,EmpForm,mentorUpdateForm,empUpdateForm
from LMS.choices import StatesOfIndia
from Support.models import *


# ==================================landing page start ==========================
def test(request):
	print(request)
	return "done" 

def index(request):
	template=loader.get_template('LMS/index.html')
	courseList = Course.objects.all()
	bundleList = Bundle.objects.all()
	
	if request.user.is_authenticated:
		final_data_list = []
		reg_courses=RegisteredCourse.objects.filter(user=request.user)
		for reg_course in reg_courses:
			try:
				group = get_object_or_404(CourseGroup, user=reg_course)
				all_users={}
				final_marks={}
				test_quizes = []	
				final_test_data={
				"tests":[],

				}
				regCourses_ = []
				final_assignment_data={}
				chapter_name=list(reg_course.course.chapter_set.all().order_by("sl_no").values_list("name", flat=True))

				for chap in reg_course.course.chapter_set.all().order_by("sl_no"):
					tests=chap.test_set.all()
					final_test_data["tests"]+=list(chap.test_set.all().values_list("name", flat=True))
				final_data={}

				for idx, each_user in enumerate(group.user.all()):
					mini_data = {
					"name":each_user.user.username,
					"data":[]
					}
					for chap in reg_course.course.chapter_set.all().order_by("sl_no"):
						tests=chap.test_set.all()
						for test in tests:
							correctanswered = Quiz.objects.filter(test=test, user__username=each_user.user.username,iscorrect=True).count()
							mini_data["data"].append(correctanswered)
					final_test_data["user"+str(idx+1)] = mini_data
				
					each_user_data={}
					each_user_data['name']=each_user.user.username
					each_user_data['data']=[]
					each_user_data['time']=[]
					chapters=reg_course.course.chapter_set.all().order_by("sl_no")
					for each_chapter in chapters:
						Chapter_assignmentresults_count=AssignmentResults.objects.filter(chapter=each_chapter, user =each_user.user, solved=True).count()
						each_user_data['data'].append(Chapter_assignmentresults_count)
						each_chapter_time=sum(list(filter(lambda x: (x != None),AssignmentResults.objects.filter(chapter=each_chapter, user=each_user.user).values_list('timetaken',flat=True))))
						each_user_data['time'].append(each_chapter_time/900)
					final_assignment_data['user'+str(idx+1)]=each_user_data
				final_assignment_data['chapters']=chapter_name
				
				
				rewards = sum(AssignmentResults.objects.filter(user=request.user).values_list("rewards", flat=True))
				last_urls = {}
				
				percent =  round(float(QuizResult.objects.filter(user = request.user, course = reg_course.course).count())/float(reg_course.course.no_of_chapters), 2)
					#"name":reg.course.id,
				try:
					not_have_last=10
					last_url1=LastActivity.objects.get(user=request.user,course=reg_course).last_url
				except:
					last_url1='/contentsDisplay/course/'+str(reg_course.id)+"/"
					not_have_last=0
				last_urls[str(reg_course.course.name)]=str(last_url1)
				final_data_list.append({"name":reg_course.course.name, "cat":reg_course.course.cat, "quizes":QuizResult.objects.filter(user = request.user, course = reg_course.course).count(), "topics":reg_course.course.no_of_chapters, "percent":percent*100, "final_assignment_data":final_assignment_data, "rewards":rewards, 'final_test_data':final_test_data, 'last_urls':last_urls,'not_have_last':not_have_last})
				print(final_data_list)
			except Exception as e:
				print(e)

			# courseCombo = zip(regCourses, regCourses_)
		context={"final_data_list":json.dumps(final_data_list), "regcourses":reg_courses}
	else:
		context={"courses":courseList, "bundles":bundleList}
	return HttpResponse(template.render(context,request))

# ==================================landing page end ==========================
# ==================================login page start ==========================
def user_login(request):
	template=loader.get_template('LMS/login.html')
	context={}
	return HttpResponse(template.render(context,request))



def courses(request):
	template=loader.get_template('LMS/courses.html')
	context={"courses" : Course.objects.all(), "bundles":Bundle.objects.all()}
	return HttpResponse(template.render(context,request))

def courseSeacrh(request):
	template=loader.get_template('LMS/coursesSearch.html')
	context={"courses" : Course.objects.filter(name__icontains=request.GET["search"]), "bundles":Bundle.objects.filter(name__icontains=request.GET["search"])}
	return HttpResponse(template.render(context,request))

def course(request, c_id):
	try:
		regCourse = RegisteredCourse.objects.get(course = Course.objects.get(id = c_id),user=request.user)
		template=loader.get_template('LMS/course.html')
		context={"regCourse":regCourse,"course" : Course.objects.get(id=c_id)}
		return HttpResponse(template.render(context,request))
	except:
		template=loader.get_template('LMS/course.html')
		context={"course" : Course.objects.get(id=c_id)}
		return HttpResponse(template.render(context,request))
		

def bundle(request, c_id):
	try:
		regBundle = RegisteredBundle.objects.get(bundle = Bundle.objects.get(id = c_id),user=request.user)
		template=loader.get_template('LMS/bundle.html')
		context={"bundle" : Bundle.objects.get(id=c_id),"regBundle":regBundle}
		return HttpResponse(template.render(context,request))
	except:
		template=loader.get_template('LMS/bundle.html')
		context={"bundle" : Bundle.objects.get(id=c_id)}
		return HttpResponse(template.render(context,request))

# ==================================cart page start ==========================

@login_required
def add_to_cart(request,cb,id):
	if cb == 'course':
		item = Course.objects.get(id=id)
		Cart.objects.get_or_create(course = item, user=Account.objects.get(email = request.user.email))
	else:
		item = Bundle.objects.get(id=id)
		Cart.objects.get_or_create(bundle = item, user=Account.objects.get(email = request.user.email))
		
	return HttpResponseRedirect("/cart")

@login_required
def cart(request):
	cart_items = Cart.objects.filter(user=Account.objects.get(email = request.user.email))
	template = loader.get_template('LMS/cart.html')
	context = {"cart_items":cart_items}
	return HttpResponse(template.render(context,request))

@login_required
def cart_item_delete(request,id):
	item = Cart.objects.get(id = id)
	item.delete()
	return HttpResponseRedirect("/cart")
	
@login_required
def cart_checkout(request,cb, id):
	item = Cart.objects.get(id = id)
	if cb == 'course':
		a=RegisteredCourse.objects.get_or_create(course = item.course, user=Account.objects.get(email = request.user.email), timetaken=0, completed_perc=0, completion_status=False)
	else:
		a,created=RegisteredBundle.objects.get_or_create(bundle = item.bundle, user=Account.objects.get(email = request.user.email), timetaken=0, completed_perc=0, completion_status=False)
		for i in a.bundle.courses.all():
			if i.id in [int(j.course.id) for j in RegisteredCourse.objects.filter(user = request.user)]:
				a.delete()
				context= {"course":i}
				template=loader.get_template('LMS/Alert.html')
				return HttpResponse(template.render(context,request))
			b=RegisteredCourse.objects.create(course = i, user=Account.objects.get(email = request.user.email), timetaken=0, completed_perc=0, completion_status=False)
	item.delete()
	# droplet=digitalocean.Droplet(token="9d38cc1038ea74a63db1c3079fd792236110ed96d965886803c08ff0b85af222",name=str(item.course),private_networking="true",region="nyc3",size="512mb",image="ubuntu-14-04-x64",ssh_keys=[Ssh.objects.get(user=request.user).key])
	# droplet.create()
	return HttpResponseRedirect('/payment')

@login_required
def cartObjects(Request):
	number = Cart.objects.all().count() 
	return JsonResponse(number, safe=False)

@login_required
def payment(request):
	template = loader.get_template('LMS/payment.html')
	context = {}
	return HttpResponse(template.render(context,request))

# ======================================= REgistered Courses ========================
@login_required
def registeredCourses(request):
	courses = RegisteredCourse.objects.filter(user=request.user)
	bundles = RegisteredBundle.objects.filter(user=request.user)
	template = loader.get_template('LMS/registeredCourses.html')
	context = {"courses":courses, "bundles":bundles}
	return HttpResponse(template.render(context,request))

# ======================================= Pretest ========================

@login_required
def pretest_landing(request,id):
	course=RegisteredCourse.objects.get(id=id,user=request.user).course
	test=pretest.objects.filter(course=course)	
	if len(pretest_results.objects.filter(user=request.user,test=test)) != len(pretest_questions.objects.filter(test=test)):
		try:
			last = pretest_results.objects.filter(user=request.user,test=test).last() 
			last_ques = last.question.id
			next_one = pretest_questions.objects.filter(id__gt=last_ques,test=last.test).order_by("id")[0]
			answers = list(next_one.pretest_answers_set.all().values().order_by("id"))
			template = loader.get_template('LMS/pretest.html')
			context = {"test":last,"first_ques":next_one,"first_answer":json.dumps(answers)}
			return HttpResponse(template.render(context,request))

		except:
			first_ques=pretest_questions.objects.filter(test=test).first()
			first_ans=list(first_ques.pretest_answers_set.all().values().order_by("id"))
			template = loader.get_template('LMS/pretest.html')
			context = {"test":test,"first_ques":first_ques,"first_answer":json.dumps(first_ans)}
			return HttpResponse(template.render(context,request))
	else:
		context = {"cb":"course","courseid":id}
		template = loader.get_template('LMS/pretestSuccess.html')
		return HttpResponse(template.render(context,request))

			

@login_required
def pretest_val(request):	
	submitted_ans_id=request.GET.get("submitted_ans")
	submitted_ans=pretest_answers.objects.get(id=submitted_ans_id)
	ques=submitted_ans.question
	correct_ans=pretest_answers.objects.get(question=ques,correct=True)
	current_user=Account.objects.get(id=request.user.id)
	test=pretest.objects.get(id=ques.test.id)
	a,created=pretest_results.objects.get_or_create(user=current_user,question=ques,test=test)
	a.submitted_ans=submitted_ans.answer
	a.correct_ans=correct_ans.answer
	if correct_ans.answer == submitted_ans.answer:
		a.iscorrect=True
		a.save()
	try:
		next_ques=pretest_questions.objects.filter(id__gt=ques.id,test=ques.test).order_by("id")[0]
		next_ques_id = next_ques.id
		next_ques_question = next_ques.question
		next_ans=list(next_ques.pretest_answers_set.all().values().order_by('id'))
		return JsonResponse({"next_ques":{"id":next_ques_id, "question":next_ques_question},"next_ans":next_ans})

	except IndexError:	

		finalresults=list(pretest_results.objects.filter(user=current_user,test=ques.test).values("question__question","submitted_ans","correct_ans","iscorrect"))
		correct=pretest_results.objects.filter(user=current_user,test=ques.test,iscorrect=True).count()
		per=(correct*100)/len(finalresults)
		r=RegisteredCourse.objects.get(course=test.course,user=request.user)
		r.pretest_score=per
		r.save()
		return JsonResponse({"cb":"course","courseid":r.id,"status":"finished"})	
		
		

# ======================================= Contents Display ========================
	
@login_required
def contentsDisplay(request,cb, id):
	if cb == 'course':
		content = RegisteredCourse.objects.get(id=id, user = request.user)
	else: 
		content = RegisteredBundle.objects.get(id=id, user=request.user)

	course = content.course
	reg_course=RegisteredCourse.objects.get(course=course,user=request.user)
	data={
	"tests":[],

	}
	for chap in course.chapter_set.all().order_by("sl_no"):
		tests=chap.test_set.all()
		data["tests"]+=list(chap.test_set.all().values_list("name", flat=True))
	final_data={}
	percent =  round(float(QuizResult.objects.filter(user = request.user, course = reg_course.course).count())/float(reg_course.course.no_of_chapters), 2)
	big_circles ={
	"name":reg_course.course.name,
	"cat":reg_course.course.cat,
	"quizes":QuizResult.objects.filter(user = request.user, course = reg_course.course).count(),
	"topics":reg_course.course.no_of_chapters,
	"percent":percent*100
	}

	print data
	template = loader.get_template('LMS/contentsDisplay.html')
	context = {'content':content, 'data':json.dumps(data), 'big_circles':json.dumps(big_circles)}
	return HttpResponse(template.render(context,request))

# ======================================= Topics and Tests Display ========================


@login_required
# def topicAndTest(request,course,chapter, page):
# 	page_sl_no = int(page)
# 	currentcourse=Course.objects.get(id=course)
# 	regCourse = RegisteredCourse.objects.get(user=request.user, course=currentcourse)
# 	chapter = Chapter.objects.get(sl_no=chapter,course=currentcourse)
# 	topics_list = list(chapter.topic_set.all().order_by("sl_no").values_list("sl_no", flat=True))
# 	test_list = list(chapter.test_set.all().order_by("sl_no").values_list("sl_no", flat=True))
# 	sorted_list = sorted(chain(topics_list, test_list))
# 	sorted_objects_list = sorted(chain(chapter.topic_set.all().order_by("sl_no"), chapter.test_set.all().order_by("sl_no")), key=lambda obj: obj.sl_no)	
# 	a = Paginator(sorted_objects_list, 1)
# 	c =  a.page(sorted_list.index(int(page))+1)
# 	if c.has_next() and c.has_previous():
# 		nextPage = a.page(c.next_page_number())
# 		prePage = a.page(c.previous_page_number())
# 		nxtpage = {"nextpagename":str(nextPage.object_list[0]),
# 			"chaptno":nextPage.object_list[0].chapter.sl_no,
# 			"topicno":nextPage.object_list[0].sl_no}
# 		prevpage = {"prevpagename":str(prePage.object_list[0]),
# 					"chaptno":prePage.object_list[0].chapter.sl_no,
# 					"topicno":prePage.object_list[0].sl_no}
# 	elif c.has_previous():
# 		prePage = a.page(c.previous_page_number())
# 		nxtpage = 0
# 		prevpage = {"prevpagename":str(prePage.object_list[0]),
# 					"chaptno":prePage.object_list[0].chapter.sl_no,
# 					"topicno":prePage.object_list[0].sl_no}
# 	elif c.has_next():
# 		nextPage = a.page(c.next_page_number())
# 		nxtpage = {"nextpagename":str(nextPage.object_list[0]),
# 			"chaptno":nextPage.object_list[0].chapter.sl_no,
# 			"topicno":nextPage.object_list[0].sl_no}		
# 		prevpage = 0
# 	elif a.count == 1:
# 		prevpage = 0
# 		nxtpage = 0	
# 	else:
# 		error = "Error in loading"
# 	try:
# 		rcourse=RegisteredCourse.objects.get(course=course,user=request.user)
# 		last_activity,c_or_n=LastActivity.objects.get_or_create(user=request.user,course=rcourse)
# 		last_activity.last_url=request.get_full_path()
# 		last_activity.save()		
# 		contents=c.object_list[0].percentage
# 		totalcount=None
# 		questions = None
# 		count=1
# 		link= "https://ibastatic.sfo2.digitaloceanspaces.com/"+str(currentcourse.cat)+'/'+str(chapter.sl_no)+'/'+str(page)+'.html'
# 		name = str(c.object_list[0])
# 		# contents = {'chapter':sl_no['chapter__sl_no'],'topic':sl_no['sl_no'],'course':sl_no['course__name']} 		
# 	except Exception as e:
# 		quest = c.object_list[0].topic.question_set.filter(level='Easy').first()
# 		totalcount=c.object_list[0].topic.question_set.all().count()
# 		count=1
# 		ans = list(quest.answer_set.all().values('ans','id'))
# 		obj,created = QuizResult.objects.get_or_create(chapter=chapter,test = c.object_list[0],user=request.user,topic=c.object_list[0].topic)
# 		questions = {'question':quest.question,'id':quest.id,"timegiven":quest.timegiven,'answers':ans}
# 		name = str(c.object_list[0])
# 		link=None
# 		contents = None	
# 	#######################navbar##################
# 	#######################

# 	if RegisteredCourse.objects.filter(course=currentcourse,user=request.user,is_grouped=True):
# 		context={"page_sl_no":page_sl_no, "regCourse":regCourse,"count":count,"link":link,"totalcount":totalcount,"next":nxtpage, "previous":prevpage,'name':name, "questions":questions,"course_grp":currentcourse.id,"courseid":course,"chapter":chapter,"page":page,"navbarElements":currentcourse}
# 		return render(request,'LMS/TopicAndTest.html',context)
# 	else:	
# 		context={"page_sl_no":page_sl_no, "regCourse":regCourse,"count":count,"link":link,"totalcount":totalcount,"next":nxtpage, "previous":prevpage,'name':name, "questions":questions,"courseid":course,"chapter":chapter,"page":page,"navbarElements":currentcourse}
# 		return render(request,'LMS/TopicAndTest.html',context)


# 	#####################
# 	chapter=a.test.chapter
# 	last_topic=chapter.topic_set.all().order_by('sl_no').last()
# 	if a.test.topic == last_topic:
# 		context={"page":page_sl_no,"regCourse":regCourse,"course_grp":chapter.course.id,"next":nxtpage, "previous":prevpage,'chaptername':a.test.chapter.name,'lastTopic':'lastTopic','count':'count finished',"courseid":chapter.course.id }
# 	else:	
# 		context={"page":page_sl_no,"regCourse":regCourse,"next":nxtpage, "previous":prevpage,"course_grp":chapter.course.id,'count':'count finished',"courseid":chapter.course.id }
# 	template=loader.get_template('LMS/TopicAndTest.html')
# 	return render(template.render(context, request))

########################### New topic and test ###########################

def topicAndTest(request,course,chapter, page):
   chapl = []
   tesl = []
   regCourse1 = RegisteredCourse.objects.filter(user=request.user)
   for each_course in regCourse1:
      ecourse = Course.objects.get(name=each_course.course.name)
      chapt = ecourse.chapter_set.all()
      for chap in chapt:
         a = QuizResult.objects.filter(user=request.user, chapter=chap)
         c = chap.problem_set.all()
         for each_problem in c:
            b = AssignmentResults.objects.filter(user=request.user, chapter=chap, problem=each_problem, solved=True)
            if (len(b) > 0):
               tesl.append(each_problem.pblm_id)
         for each_topic in a:
               tesl.append(each_topic.topic.name)
               tesl.append(each_topic.test.name)
      chapl.append(chap.name)
   page_sl_no = int(page)
   currentcourse=Course.objects.get(id=course)
   regCourse = RegisteredCourse.objects.filter(user=request.user, course=currentcourse)
   chapter = Chapter.objects.get(sl_no=chapter,course=currentcourse)
   topics_list = list(chapter.topic_set.all().order_by("sl_no").values_list("sl_no", flat=True))
   test_list = list(chapter.test_set.all().order_by("sl_no").values_list("sl_no", flat=True))
   sorted_list = sorted(chain(topics_list, test_list))
   sorted_objects_list = sorted(chain(chapter.topic_set.all().order_by("sl_no"), chapter.test_set.all().order_by("sl_no")), key=lambda obj: obj.sl_no)    
   a = Paginator(sorted_objects_list, 1)
   c =  a.page(sorted_list.index(int(page))+1)
   if c.has_next() and c.has_previous():
      nextPage = a.page(c.next_page_number())
      prePage = a.page(c.previous_page_number())
      nxtpage = {"nextpagename":str(nextPage.object_list[0]),
         "chaptno":nextPage.object_list[0].chapter.sl_no,
         "topicno":nextPage.object_list[0].sl_no}
      prevpage = {"prevpagename":str(prePage.object_list[0]),
               "chaptno":prePage.object_list[0].chapter.sl_no,
               "topicno":prePage.object_list[0].sl_no}
   elif c.has_previous():
      prePage = a.page(c.previous_page_number())
      nxtpage = 0
      prevpage = {"prevpagename":str(prePage.object_list[0]),
               "chaptno":prePage.object_list[0].chapter.sl_no,
               "topicno":prePage.object_list[0].sl_no}
   elif c.has_next():
      nextPage = a.page(c.next_page_number())
      nxtpage = {"nextpagename":str(nextPage.object_list[0]),
         "chaptno":nextPage.object_list[0].chapter.sl_no,
         "topicno":nextPage.object_list[0].sl_no}      
      prevpage = 0
   elif a.count == 1:
      prevpage = 0
      nxtpage = 0    
   else:
      error = "Error in loading"
   try:      
      contents=c.object_list[0].percentage
      totalcount=None
      questions = None
      count=1
      link= "https://ibastatic.sfo2.digitaloceanspaces.com/"+str(currentcourse.cat)+'/'+str(chapter.sl_no)+'/'+str(page)+'.html'
      name = str(c.object_list[0])
      # contents = {'chapter':sl_no['chapter__sl_no'],'topic':sl_no['sl_no'],'course':sl_no['course__name']}
   except Exception as e:
      quest = c.object_list[0].topic.question_set.filter(level='Easy').first()
      totalcount=c.object_list[0].topic.question_set.all().count()
      count=1
      ans = list(quest.answer_set.all().values('ans','id'))
      obj,created = QuizResult.objects.get_or_create(chapter=chapter,test = c.object_list[0],user=request.user,topic=c.object_list[0].topic)
      questions = {'question':quest.question,'id':quest.id,"timegiven":quest.timegiven,'answers':ans}
      name = str(c.object_list[0])
      link=None
      contents = None
   regC= RegisteredCourse.objects.get(user=request.user, course=currentcourse)
   #######################navbar##################
   #######################
   if RegisteredCourse.objects.filter(course=currentcourse,user=request.user,is_grouped=True):
      context={"page_sl_no":page_sl_no, "regCourse":regCourse,"count":count,"link":link,
             "totalcount":totalcount,"next":nxtpage, "previous":prevpage,'name':name, "questions":questions,
             "course_grp":currentcourse.id,"courseid":course,
             "chapter":chapter,"page":page,"navbarElements":currentcourse,"test":tesl,"regC":regC}
      return render(request,'LMS/TopicAndTest.html',context)
   else:  
      context={"page_sl_no":page_sl_no, "regCourse":regCourse,
             "count":count,"link":link,"totalcount":totalcount,"next":nxtpage,
             "previous":prevpage,'name':name, "questions":questions,"courseid":course,
             "chapter":chapter,"page":page,"navbarElements":currentcourse, "test":tesl,"regC":regC}
      return render(request,'LMS/TopicAndTest.html',context)
   #####################
   chapter=a.test.chapter
   last_topic=chapter.topic_set.all().order_by('sl_no').last()
   if a.test.topic == last_topic:
      context={"page":page_sl_no,"regCourse":regCourse,"course_grp":chapter.course.id,"next":nxtpage, "previous":prevpage,
	  'chaptername':a.test.chapter.name,'lastTopic':'lastTopic','count':'count finished',"courseid":chapter.course.id,"test":tesl,"regC":regC }
   else:  
      context={"page":page_sl_no,"regCourse":regCourse,"next":nxtpage, "previous":prevpage,"course_grp":chapter.course.id,'count':'count finished',
	  "courseid":chapter.course.id, "test":tesl,"regC":regC}
   template=loader.get_template('LMS/TopicAndTest.html')
   return render(template.render(context, request))

########################### End of New topic and test####################
############################# Test Validate ###########
@csrf_exempt
# def Testvalidate(request,count):
# 	print(ast.literal_eval(request.POST.get('next')))
# 	print(type(request.POST.get('next')))	
# 	totalcount = int(request.POST.get('totalcount'))
# 	prevcount = int(count)
# 	'''		result status        '''
# 	cu_user=request.user
# 	submited_quest = Question.objects.get(id = request.POST.get('questionid'))
# 	test =submited_quest.test
# 	ans_submited = submited_quest.answer_set.values('correct','ans').get(id = request.POST.get('answer'))
# 	correct_ans = str(submited_quest.answer_set.get(correct = True))
# 	regCourse = RegisteredCourse.objects.get(user=request.user, course=submited_quest.chapter.course.id)
# 	'''		Test Result storing		'''

# 	# TestResult.objects.create(test_course=test.chapter.course,test_topic=test.topic,test_percent = 0, test_timetaken= float(request.POST['time_taken']), test_test=test, ans_records=request.POST['answer'])
	
# 	obj,created = Quiz.objects.get_or_create(user = request.user ,test = test,topic = test.topic,question = submited_quest,corct_ans = correct_ans, difficulty = submited_quest.level)
# 	obj.ans_submit = ans_submited['ans']
# 	obj.iscorrect = ans_submited['correct']
# 	obj.timetaken = abs(int(request.POST.get("timegiven"))- int((request.POST.get("timeTaken"))))
# 	obj.save()
# 	result = {'submited_quest':str(submited_quest),'submitted_ans':ans_submited['ans'],'correct_ans':correct_ans}
# 	subtopics = list(subTopic.objects.filter(topic=test.topic).order_by("id"))
# 	if prevcount < totalcount:
# 		prevcount = prevcount + 1
# 		next_question = Question.objects.filter(id__gt = request.POST.get('questionid'), test=test).order_by("id")[0]
# 	else :
# 		final_result = list(Quiz.objects.filter(test=test,user=cu_user).values('question__question','user','ans_submit','corct_ans','iscorrect','timetaken','difficulty'))
# 		correct = Quiz.objects.filter(test=test,user=cu_user,iscorrect=True).count()
# 		a, created=QuizResult.objects.get_or_create(user=cu_user,test=test)
# 		print(correct)
# 		print(len(final_result))
# 		a.quiz_percentile =(correct*100)/len(final_result)
# 		print(a.quiz_percentile)
# 		a.save()

# 		#####################
# 		chapter=a.test.chapter
# 		last_topic=chapter.topic_set.all().order_by('sl_no').last()
# 		if a.test.topic == last_topic:
# 			context={"regCourse":regCourse,"course_grp":chapter.course.id,"navbarElements":obj.topic.chapter.course,'name':test.name,'chaptername':a.test.chapter.name,"chapter":chapter,'lastTopic':'lastTopic','final_result':final_result,'count':'count finished','test_percentile':a.quiz_percentile , }
# 		else:	
# 			context={"regCourse":regCourse,"course_grp":chapter.course.id,"navbarElements":obj.topic.chapter.course,'name':test.name,"next":ast.literal_eval(request.POST.get('next')),"previous":ast.literal_eval(request.POST.get('previous')),'final_result':final_result,'count':'count finished','test_percentile':a.quiz_percentile }
# 		return render(request,'LMS/TopicAndTest.html',context)
# 	ans = list(next_question.answer_set.all().values('ans','id'))
# 	tags = list(next_question.tag.all())
# 	question = {'question':next_question.question,'id':next_question.id,"timegiven":next_question.timegiven,'answers':ans}
# 	context={"regCourse":regCourse,"course_grp":submited_quest.topic.chapter.course.id,"navbarElements":obj.topic.chapter.course,'name':test.name,"questions":question,"count":prevcount,"totalcount":totalcount,"next":ast.literal_eval(request.POST.get('next')),"previous":ast.literal_eval(request.POST.get('previous'))}
# 	return render(request,'LMS/TopicAndTest.html',context)
############################### New Test validate ################################
def Testvalidate(request,count):
   # print(ast.literal_eval(request.POST.get('next')))
   # print(type(request.POST.get('next')))
   totalcount = int(request.POST.get('totalcount'))
   prevcount = int(count)
   '''       result status        '''
   cu_user=request.user
   submited_quest = Question.objects.get(id = request.POST.get('questionid'))
   test =submited_quest.test
   ans_submited = submited_quest.answer_set.values('correct','ans').get(id = request.POST.get('answer'))
   correct_ans = str(submited_quest.answer_set.get(correct = True))
   regCourse = RegisteredCourse.objects.get(user=request.user, course=submited_quest.chapter.course.id)
   '''       Test Result storing       '''
   # TestResult.objects.create(test_course=test.chapter.course,test_topic=test.topic,test_percent = 0, test_timetaken= float(request.POST['time_taken']), test_test=test, ans_records=request.POST['answer'])
   obj,created = Quiz.objects.get_or_create(user = request.user ,test = test,topic = test.topic,question = submited_quest,corct_ans = correct_ans, difficulty = submited_quest.level)
   obj.ans_submit = ans_submited['ans']
   obj.iscorrect = ans_submited['correct']
   obj.timetaken = abs(int(request.POST.get("timegiven"))- int((request.POST.get("timeTaken"))))
   obj.save()
   result = {'submited_quest':str(submited_quest),'submitted_ans':ans_submited['ans'],'correct_ans':correct_ans}
   subtopics = list(subTopic.objects.filter(topic=test.topic).order_by("id"))

  ################################ completed activities #######################
   chaptl = []
   testl = []
   regCourse1 = RegisteredCourse.objects.filter(user=request.user)
   for each_course in regCourse1:
      ecourse = Course.objects.get(name=each_course.course.name)
      chapt = ecourse.chapter_set.all()
      for chap in chapt:
         a = QuizResult.objects.filter(user=request.user, chapter=chap)
         c = chap.problem_set.all()
         for each_problem in c:
            b = AssignmentResults.objects.filter(user=request.user, chapter=chap, problem=each_problem, solved=True)
            if (len(b) > 0):
               testl.append(each_problem.pblm_id)
         for each_topic in a:
            testl.append(each_topic.topic.name)
            testl.append(each_topic.test.name)
      chaptl.append(chap.name)
   courseid=submited_quest.topic.chapter.course.id
   #############################

   if prevcount < totalcount:
      prevcount = prevcount + 1
      next_question = Question.objects.filter(id__gt = request.POST.get('questionid'), test=test).order_by("id")[0]
   else :
      final_result = list(Quiz.objects.filter(test=test,user=cu_user).values('question__question','user','ans_submit','corct_ans','iscorrect','timetaken','difficulty'))
      correct = Quiz.objects.filter(test=test,user=cu_user,iscorrect=True).count()
      a, created=QuizResult.objects.get_or_create(user=cu_user,test=test)
      print(correct)
      print(len(final_result))
      a.quiz_percentile =(correct*100)/len(final_result)
      print(a.quiz_percentile)
      a.save()
      #####################
	  
      chapter=a.test.chapter
      last_topic=chapter.topic_set.all().order_by('sl_no').last()
      if a.test.topic == last_topic:
         context={"regCourse":regCourse,"course_grp":chapter.course.id,"navbarElements":obj.topic.chapter.course,
		 'name':test.name,'chaptername':a.test.chapter.name,"chapter":chapter,'lastTopic':'lastTopic',
		 'final_result':final_result,'count':'count finished','test_percentile':a.quiz_percentile ,"test":testl,"regC":regCourse, "courseid":courseid }
      else:  
         context={"regCourse":regCourse,"course_grp":chapter.course.id,"navbarElements":obj.topic.chapter.course,
		 'name':test.name,"next":ast.literal_eval(request.POST.get('next')),"previous":ast.literal_eval(request.POST.get('previous')),
		 'final_result':final_result,'count':'count finished','test_percentile':a.quiz_percentile,"test":testl,"regC":regCourse, "courseid":courseid }
      return render(request,'LMS/TopicAndTest.html',context)
   ans = list(next_question.answer_set.all().values('ans','id'))
   tags = list(next_question.tag.all())
   question = {'question':next_question.question,'id':next_question.id,"timegiven":next_question.timegiven,'answers':ans}
 
   context={"regCourse":regCourse,"course_grp":submited_quest.topic.chapter.course.id,
          "navbarElements":obj.topic.chapter.course,'name':test.name,"questions":question,
          "count":prevcount,"totalcount":totalcount,"next":ast.literal_eval(request.POST.get('next')),
          "previous":ast.literal_eval(request.POST.get('previous')),"test":testl,"regC":regCourse, "courseid":courseid }
   return render(request,'LMS/TopicAndTest.html',context)

############################### End of New Test validate ################################

@login_required
def TestOverview(request,courseid, chapterid):
	chapter = Chapter.objects.get(course=Course.objects.get(id=courseid),sl_no=chapterid)
	print(chapter.topic_set.all().order_by("sl_no"))
	score=chapter.quizresult_set.filter(user=request.user)
	# print([{"topic":i.name,  "result":QuizResult.objects.get(topic=i, user=request.user)}for i in chapter.topic_set.all()])
	knowledgeScore =sum(i.quiz_percentile for i in score)
	problemid = Problem.objects.filter(chapter=chapter).first()
	context={'problemid':problemid,'chapter':chapter,'score':score,'knowledgeScore':knowledgeScore/score.count()}
	return render(request,"LMS/TestOverview.html",context)
	


#----------------------------------Assignments old------------------------------------------

# def Assignments(request,a):
# 	pbm_id=Problem.objects.get(id=a)
# 	currentuser = Account.objects.get(email=request.user.email)
# 	pages = [pbm["id"] for pbm in pbm_id.chapter.problem_set.all().values("id")]
# 	if pages.index(int(a)) +1 == len(pages):
# 		next_page= False
# 		next_page_num = 0
# 		previous_page = True
# 		previous_page_num = pages[pages.index(int(a)) -1]
# 	elif pages.index(int(a)) == 0:
# 		previous_page = False
# 		next_page = True
# 		previous_page_num = pages[pages.index(int(a)) -1]
# 		next_page_num = pages[pages.index(int(a))+1]
# 	else:
# 		previous_page = True
# 		previous_page_num = pages[pages.index(int(a))-1]
# 		next_page_num = pages[pages.index(int(a))+1]
# 		next_page = True
# 	mode='python'
# 	try:
# 		Assignmentresults = AssignmentResults.objects.get( problem=pbm_id,user =request.user)
# 		context={"Assignmentresults":Assignmentresults,"currentuser":currentuser.id,"problem":pbm_id,"mode":mode,"previous_page":previous_page,"next_page":next_page,"previous_page_num":previous_page_num,"next_page_num":next_page_num}
# 		template=loader.get_template('LMS/Assignments.html')
# 		return HttpResponse(template.render(context,request))
		
# 	except:	
# 		context={"currentuser":currentuser.id,"problem":pbm_id,"mode":mode,"previous_page":previous_page,"next_page":next_page,"previous_page_num":previous_page_num,"next_page_num":next_page_num}
# 		template=loader.get_template('LMS/Assignments.html')
# 		return HttpResponse(template.render(context,request))





#===================================== New Assignments========================================

@login_required
def Assignments(request, a):
   pbm_id = Problem.objects.get(id=a)
   courseid = pbm_id.chapter.course.id
   regCourse = RegisteredCourse.objects.get(user=request.user, course=pbm_id.chapter.course)
   ch = []
   chapter = list(regCourse.course.chapter_set.all().values("id"))
   for i in chapter:
      ch.append(i['id'])
   ch_l = range(0, len(ch))
   currentuser = Account.objects.get(email=request.user.email)
   pages = [pbm["id"] for pbm in pbm_id.chapter.problem_set.all().values("id").order_by("id")]
   if pages.index(int(a)) + 1 == len(pages):
      next_page = False
      next_page_num = 0
      previous_page = True
      previous_page_num = pages[pages.index(int(a)) - 1]
   elif pages.index(int(a)) == 0:
      previous_page = False
      next_page = True
      previous_page_num = pages[pages.index(int(a)) - 1]
      next_page_num = pages[pages.index(int(a)) + 1]
   else:
      previous_page = True
      previous_page_num = pages[pages.index(int(a)) - 1]
      next_page_num = pages[pages.index(int(a)) + 1]
      next_page = True
   mode = 'python'
   ################################ completed activities #######################
   chaptl = []
   testl = []
   regCourse1 = RegisteredCourse.objects.filter(user=request.user)
   for each_course in regCourse1:
      ecourse = Course.objects.get(name=each_course.course.name)
      chapt = ecourse.chapter_set.all()
      A = []
      C = []
      for chap in chapt:
         a = QuizResult.objects.filter(user=request.user, chapter=chap)
         if (len(a) > 0):
            A.append(a)
            for each_topic in a:
               testl.append(each_topic.test.name)
               testl.append(each_topic.topic.name)
         c = chap.problem_set.all()
         for each_problem in c:
            b = AssignmentResults.objects.filter(user=request.user, chapter=chap, problem=each_problem, solved=True)
            if (len(b) > 0):
               testl.append(each_problem.pblm_id)
      chaptl.append(chap.name)
   #############################
   # try:
   Assignmentresults, created = AssignmentResults.objects.get_or_create(problem=pbm_id, user=request.user,
                                                       chapter=pbm_id.chapter)
   anp = pbm_id.testcases_set.all().order_by("testCase")
   amp = (getattr(Assignmentresults, "testcase1"), getattr(Assignmentresults, "testcase2"),
         getattr(Assignmentresults, "testcase3"))
   thirrr = zip(amp, anp)
   context = {"thirrr": thirrr, "navbarElements": pbm_id.chapter.course,
            "course_grp": pbm_id.chapter.course.id, "Assignmentresults": Assignmentresults,
            "currentuser": currentuser.id, "problem": pbm_id, "mode": mode,
            "previous_page": previous_page, "next_page": next_page,
            "previous_page_num": previous_page_num, "next_page_num": next_page_num,
            "regCourse": regCourse, "pbm_id": pbm_id, "ch": ch, "ch_l": ch_l,"test":testl,"regC":regCourse,
            "courseid":courseid}
   template = loader.get_template('LMS/Assignments.html')
   return HttpResponse(template.render(context, request))
# except:
#  context={"course_grp":pbm_id.chapter.course.id,"currentuser":currentuser.id,"problem":pbm_id,"mode":mode,"previous_page":previous_page,"next_page":next_page,"previous_page_num":previous_page_num,"next_page_num":next_page_num}
#  template=loader.get_template('LMS/Assignments.html')
#  return HttpResponse(template.render(context,request))



#++++++++++++++++++++++++++++++++ End of New Assignments =====================================

@csrf_exempt
def compiler(request):
	url = "http://157.245.96.100/compiler/" 
	dat = {'file' : request.POST.get("file")}
	data = urllib.urlencode(dat)
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	outcome = response.read()
	outcome=outcome.replace("<","&lt;").replace(">","&gt;")	
	return JsonResponse(outcome,safe=False)

@csrf_exempt
@login_required
def testcase(request):
	# pblm = Problem.objects.get(id=request.POST.get("p_id", None))
	# testCaseObj = TestCases.objects.get(id=request.POST.get("id", None))
	# a = testCaseObj.testCase
	# assignmentResultObj = AssignmentResults.objects.get_or_create(chapter=pblm.chapter, problem=pblm, user =request.user)
	# assignmentResultObj[0].attemps = assignmentResultObj[0].attemps + 1 
	# if request.POST.get("value", None) == testCaseObj.correct_ans:
	# 	if testCaseObj.testCase == "testcase1":
	# 		assignmentResultObj[0].testcase1 = True
	# 		assignmentResultObj[0].rewards = pblm.rewards
	# 		assignmentResultObj[0].save()
	# 	elif testCaseObj.testCase == "testcase2":
	# 		assignmentResultObj[0].testcase2 = True
	# 		assignmentResultObj[0].save()
	# 	else:
	# 		assignmentResultObj[0].testcase3 = True
	# 		assignmentResultObj[0].save()
	# 	return JsonResponse({"id":request.POST.get("id"), "status":200, "re":"True"})
	# else:
	# 	return JsonResponse({"id":request.POST.get("id"), "status":400, "re":"False"})

	number = request.POST.get("number",0) 
	problem = request.POST.get("problemid")
	currentuser = request.POST.get("currentuser")
	timeTaken=request.POST.get("timeTaken")
	url = "http://157.245.96.100/compiler/" 
	dat = {'file' : request.POST.get("file")}
	data = urllib.urlencode(dat)
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	output = response.read()
	outcome = json.loads(output)
	result = [str(r) for r in outcome["output"]]
	pblm = Problem.objects.get(id = problem)
	Assignmentresults, created = AssignmentResults.objects.get_or_create(chapter=pblm.chapter, problem=pblm, user =Account.objects.get(id=currentuser))
	finalresult=str(result).replace("'",'"')
	
	if int(number) == 1:
		if finalresult == eval(json.dumps(pblm.testcase1Output)):

			Assignmentresults.testcase1 = True
			Assignmentresults.timetaken = abs(pblm.timegiven-timeTaken)
			if Assignmentresults.testcase2 == Assignmentresults.testcase3 == True:
				Assignmentresults.solved=True
			Assignmentresults.save()
			return JsonResponse({"status":1,"verified":"yes","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)
		else:
			return JsonResponse({"status":1,"verified":"not verified","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)
	elif int(number) == 2:
		if finalresult == eval(json.dumps(pblm.testcase2Output)):
			Assignmentresults.testcase2 = True
			Assignmentresults.timetaken = abs(pblm.timegiven-timeTaken)
			if Assignmentresults.testcase1 == Assignmentresults.testcase3 == True:
				Assignmentresults.solved=True
			Assignmentresults.save()
			return JsonResponse({"status":2,"verified":"yes","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)
		else:
			return JsonResponse({"status":2,"verified":"not verified","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)
	elif int(number) == 3:
		if finalresult == eval(json.dumps(pblm.testcase3Output)):
			Assignmentresults.testcase1 = True
			Assignmentresults.timetaken = abs(pblm.timegiven-timeTaken)
			if Assignmentresults.testcase2 == Assignmentresults.testcase3 == True:
				Assignmentresults.solved=True
			Assignmentresults.save()
			return JsonResponse({"status":3,"verified":"yes","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)
		else:
			return JsonResponse({"status":3,"verified":"not verified","output":output.replace("<","&lt;").replace(">","&gt;")},safe=False)



@login_required
def chapterOverview(request,a,b):
	chapter = Chapter.objects.get(id=b)
	registeredCourse_content_display = RegisteredCourse.objects.get(course__id = a, user=request.user).id 
	course_id = a
	try:
		next_chapter = Chapter.objects.filter(id__gt=b,course__id=course_id).order_by('id')[0]
		next_topic = next_chapter.topic_set.all().values('sl_no').first()
	except:
		next_chapter = None
		next_topic =None

	testResults = QuizResult.objects.filter(test__chapter=chapter,user=request.user).values('topic__name','Easy_percentile','Intermediate_percentile','Difficult_percentile','quiz_percentile')
	assignmentResults = AssignmentResults.objects.filter(chapter=chapter,user=request.user).values('problem_id__pblm_id','testcase1','testcase2','testcase3','timetaken')
	template=loader.get_template('LMS/chapterOverview.html')
	context={"registeredCourse_content_display":registeredCourse_content_display, "course_grp":course_id, 'course_id':course_id,'chapter':chapter,"testResults":testResults,"assignmentResults":assignmentResults,'course_grp':course_id}
	return HttpResponse(template.render(context,request))
	
#==============================================Grouping=========================================
def chunks(li,n):
		final=[[],[],[],[],[]]
		final[0].extend(li[0:n])
		final[1].extend(li[n:(n+n)])
		final[2].extend(li[(n+n):(n+n+n)])
		final[3].extend(li[(n+n+n):(n+n+n+n)])
		final[4].extend(li[(n+n+n+n):(n+n+n+n+n)])
		return final

@login_required
def CourseGrouping(request):
	courses=Course.objects.all()
	groupMembersList=[]
	for i in courses:
		groupMembersList.append({   #filter needs to be added for users 
		str(i):chunks(list( i.registeredcourse_set.filter(is_grouped=False).order_by('pretest_score')),len(list( i.registeredcourse_set.filter(is_grouped=False).order_by('pretest_score')))//5)
		})	
	for i in groupMembersList:
		for key,value in i.iteritems():
			if value[0] != []:
				x1=value[0]
				x2=reversed(value[1])
				x3=value[2]
				x4=reversed(value[3])
				x5=value[4]
				for (i,j, k,l,m) in zip(x1,x2,x3,x4,x5):					
					g=CourseGroup.objects.create(name=str(key)+str(randint(100000,1000000)),course=i.course)
					g.user.add(i.id,j.id,k.id,l.id,m.id)
					g.save()
					i.is_grouped,j.is_grouped,k.is_grouped,l.is_grouped,m.is_grouped=(True,)*5
					i.save()
					j.save()
					k.save()
					l.save()
					m.save()
			else:
				pass
	return HttpResponse('ding')

@login_required
def groupsDisplay(request):
	courseid=request.GET['courseid']
	course=Course.objects.get(id=courseid)
	reg_course=RegisteredCourse.objects.get(course=course,user=request.user)
	group=CourseGroup.objects.get(user=reg_course)
	# print(group)
	group_mem = list(group.user.exclude(user=request.user).values('user__username','user_id','course__id'))
	
	# #======== last active =========	
	for i in group_mem:
		A2A_Rewards=len(QueryAnswer.objects.filter(answered_by=Account.objects.get(id=i["user_id"]),rewards=1))
		assessment_rewards=len(Quiz.objects.filter(user=Account.objects.get(id=i["user_id"]),iscorrect=True))
		user1 = OnlineUserActivity.objects.get(user__id=i["user_id"])
		reqtime = datetime.now() - timedelta(minutes = 10)
		i['rewards'] = A2A_Rewards+assessment_rewards
		if user1.last_activity <= reqtime :
			i["lastActivity"] = "offline"
		else:
			i["lastActivity"] = "online"
	userslist=list(group.user.all().exclude(user=request.user).values_list("user__id",flat=True))
	#======== last active =========	

	return JsonResponse(group_mem,safe=False)




#=============
@login_required
def test_creation(request):
	
	if request.method=='POST':
		test=Test.objects.create(name=request.POST['test'],chapter=Chapter.objects.get(id=request.POST['chapter']),topic=Topic.objects.get(id=request.POST['topic']))
		return redirect('/test_ques/'+str(test.id))
	else:
		template=loader.get_template('LMS/test_creation_form.html')
		courses=Course.objects.all()
		context={'courses':courses}
		return HttpResponse(template.render(context,request))
	

@login_required
def test_ques(request,a):
	# try:
	if request.method=='POST':
		test_id=request.POST['test_id']

		test=Test.objects.get(id=request.POST['test_id'])

		ques=Question.objects.create(test=test,topic=test.topic,question=request.POST['question'],chapter=test.chapter,level=request.POST["level"])
		ans1=Answer.objects.create(ans=request.POST['answer1'],question=ques,correct=request.POST.get("checkbox1", False))
		ans2=Answer.objects.create(ans=request.POST['answer2'],question=ques,correct=request.POST.get("checkbox2", False))
		ans3=Answer.objects.create(ans=request.POST['answer3'],question=ques,correct=request.POST.get("checkbox3", False))
		ans4=Answer.objects.create(ans=request.POST['answer4'],question=ques,correct=request.POST.get("checkbox4", False))
		return HttpResponseRedirect('/test_ques/'+str(test.id))

	else:
		template=loader.get_template('LMS/test_ques_form.html')
		context={'test_id':a}
		return HttpResponse(template.render(context,request))
	# except Exception as e:
	# 	template=loader.get_template('LMS/error_message.html')
	# 	context={
	# 	'error':e
	# 	}
	# 	return HttpResponse(template.render(context,request))
	
@login_required
def chapt_topic_ajax(request,a):
	course=Course.objects.get(id=a)
	chapters=list(course.chapter_set.all().order_by("sl_no"))
	chapterslist=list(course.chapter_set.all().values("id", "name"))
	topicslist={}
	for i in chapters:
			topicslist[i.id]=list(i.topic_set.all().values("id", "name"))
	return JsonResponse({'topicslist':topicslist,'chapterslist':chapterslist})

@login_required
def coursesList(result):
	courses= list(Course.objects.all().values("id","name"))
	return JsonResponse({'courseslist':courses})




# def testDDPG(sess, env, actor, critic, newth):


#     # test for max_episodes number of episodes
#     # for i in range(int(1)):

#     s = env.reset()

#     ep_reward = 0
#     ep_ave_max_q = 0

#     #if action =='store_true':
#         #env.render()
    

#     a = actor.predict(np.reshape(s, (1, actor.s_dim))) 

   
#     s2, r, terminal, info = env.step(a[0], newth)

   
#     s = s2
#     ep_reward += r

#         # if terminal:
#         #     print('| Episode: {:d} | Reward: {:d} |'.format(i, int(ep_reward)))
#         #     break
#     print("************************ new value****************")
#     print(a)
#     print("************************ new value****************")
#     return (a)
    # return a
    
# def test(request):
#     with tf.Session() as sess:

#         env = gym.make('shal-v0')
#         np.random.seed(258)
#         tf.set_random_seed(258)
#         env.seed(258)
#         env._max_episode_steps = 1000

#         state_dim = env.observation_space.shape[0]
#         action_dim = env.action_space.shape[0]
#         action_bound = env.action_space.high

#         actor = ActorNetwork(sess, state_dim, action_dim, action_bound,
#                 float(0.0001), float(0.001), int(64))

#         critic = CriticNetwork(sess, state_dim, action_dim,
#                  float(0.001), float(0.001), float(0.99), actor.get_num_trainable_vars())

#         saver = tf.train.Saver()
#         saver.restore(sess, "LMS/ckpt/model")

#         #testDDPG(sess, env, args, actor, critic)
#         ping = testDDPG(sess, env, actor, critic, float(request.GET.get("newth", 0)))
#         return HttpResponse(ping)




# @csrf_exempt
# def testcase(request):
# 	number = request.POST.get("number",0) 
# 	problem = request.POST.get("problemid")
# 	currentuser = request.POST.get("currentuser")
# 	url = "http://157.245.96.100/compiler/" 
# 	dat = {'file' : request.POST.get("file")}
# 	data = urllib.urlencode(dat)
# 	request = urllib2.Request(url, data)
# 	response = urllib2.urlopen(request)
# 	output = response.read()
# 	outcome = json.loads(output)
# 	result = [str(r) for r in outcome["output"]]
# 	pblm = Problem.objects.get(id = problem)
# 	Assignmentresults, created = AssignmentResults.objects.get_or_create( problem=pblm,user =Account.objects.get(id=currentuser))
# 	if int(number) == 1:
# 		if str(result) == eval(json.dumps(pblm.testcase1Output)):
# 			Assignmentresults.testcase1 = True
# 			Assignmentresults.save()
# 			return JsonResponse({"status":1,"verified":"yes","output":output},safe=False)
# 		else:
# 			return JsonResponse({"status":1,"verified":"not verified","output":output},safe=False)
# 	elif int(number) == 2:
# 		if str(result) == eval(json.dumps(pblm.testcase2Output)):
# 			Assignmentresults.testcase2 = True
# 			Assignmentresults.save()
# 			return JsonResponse({"status":2,"verified":"yes","output":output},safe=False)
# 		else:
# 			return JsonResponse({"status":2,"verified":"not verified","output":output},safe=False)
# 	elif int(number) == 3:
# 		if str(result) == eval(json.dumps(pblm.testcase3Output)):
# 			Assignmentresults.testcase1 = True
# 			Assignmentresults.save()
# 			return JsonResponse({"status":3,"verified":"yes","output":output},safe=False)
# 		else:
# 			return JsonResponse({"status":3,"verified":"not verified","output":output},safe=False)



@csrf_exempt
@login_required
def saveProblem(request):
	print request.POST["currentuser"]
	print request.POST["file"]
	print request.POST["problemid"]
	return JsonResponse({"message":"Saved", status:200})






