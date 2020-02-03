# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned,ValidationError
from django.contrib.auth import update_session_auth_hash,hashers
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django_project.settings import STATIC_ROOT, MEDIA_ROOT,EMAIL_HOST_USER
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
# Create your views here.
from .models import *
import string
from random import randint, choice
from LMS.models import *
def user_register(request):
	if request.method=='POST':
		try:
			try:
				a=validate_email(request.POST['email'])
			except ValidationError as e:
				return JsonResponse("Enter a valid email address",safe=False)
			characters = string.ascii_letters + string.digits
			passcode =  ("".join(choice(characters) for x in range(randint(6,8)))).upper()		
			acc = Account.objects.create_user(location = request.POST['locations'],email = request.POST['email'], password = request.POST['password1'],username=request.POST['username'], phone_number = request.POST['phone_number'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],address=request.POST['address'] , acc_key = passcode )
			# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			# msg.attach_alternative(html_content, "text/html")
			# msg.send()
			email = EmailMessage(subject='verify Account', body=passcode, from_email='admin@metagogyai.com', to=[acc.email])
			email.send()
			# send_mail('verify Account',passcode, "gopi@metagogyai.com", [acc.email])
			message = ''' 
					Registered Successfully, An Email with conformation code is sent to registered email .
					Use the secret code at the time of login for verifying the mail you registered with us .
				  '''
			context = {"message":message}
			return render(request,"Users/passcode.html",context)
		except Exception as e:
			error = {	'UNIQUE constraint failed: Users_account.email':'email already exists',
						'UNIQUE constraint failed: Users_account.username':'username exists , try another',
						'UNIQUE constraint failed: Users_account.phone_number':'Account already registered with this phone_number '
					}
			print (e)
			context = { "error" : str(error[str(e)]) }
			return render(request , "Users/passcode.html" , context )
	else:
		states=StatesOfIndia.get_state_names()
		context = {'states':states}
		return render(request,"Users/user_register.html" ,context)
			
def verifyAccount(request):
	try:
		key = request.POST.get("key")
		acc = Account.objects.get(acc_key=key)
		if  acc is not None :
			acc.is_verified = True
			acc.save()
			auth_login(request, acc,backend='django.contrib.auth.backends.ModelBackend')
			return redirect("/")
	except Exception as e:
		context = {"error": "Submitted code doesnt match any account ."}
		return render(request, "Users/accountverify.html", context)
   
def login_auth(request):
	try:
		username = request.POST.get("user_name")
		password = request.POST.get("password")
		userr = authenticate(username=username, password=password)
		if userr is not None:
			myaccount=Account.objects.get(email=username)
			if myaccount.is_verified == False:
				context = {"user": userr}
				template = loader.get_template("Users/accountverify.html")
				return HttpResponse(template.render(context, request))
			else:
				login(request, userr)
				return HttpResponseRedirect("/")
		else:
			template = loader.get_template("LMS/login.html")
			context = {"error": "Invalid credentials"}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template = loader.get_template("LMS/login.html")
		context = {"error": "Invalid credentials"}
		return HttpResponse(template.render(context, request))

@login_required
def logout_view(request):
	try:
		logout(request)
		return HttpResponseRedirect("/")
	except Exception as e:
		template=loader.get_template('Users/error_message.html')
		context={
		'error':"Failed To Load Logout Please Try Again "
		}
		return HttpResponse(template.render(context,request))

@login_required
def changePassword(request):
	if request.method == 'POST':
		if request.POST['newPassword'] == request.POST['newPassword1'] :
			try : 
				val = hashers.check_password(request.POST['oldPassword'],request.user.password)
				if val:
					user = request.user
					user.set_password(request.POST['newPassword'])
					user.save()
					return redirect("/")
				else : 
					raise Exception("Please enter the correct password")
			except Exception as e:
				context = {'error' : str(e) }
			return render(request,"Users/changePassword.html",context)
		else:
			context = {'error':"Entered passwords doesnt match "}
			return render(request,"Users/changePassword.html",context)
	else :
		return render(request,"Users/changePassword.html")

@login_required
def profile(request):
	regCourses = RegisteredCourse.objects.filter(user=request.user).count()
	rewards = sum(AssignmentResults.objects.filter(user=request.user).values_list("rewards", flat=True))
	context = {"regCourses":regCourses, "rewards":rewards}
	return render(request,"Users/profile.html",context)