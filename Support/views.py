from __future__ import unicode_literals
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from Support.models import *
from django.views.generic.edit import UpdateView
from .forms import EditanswerForm,EditQuestionForm
from datetime import datetime, timedelta, date
from operator import and_, or_
from django.db.models import Q
import __builtin__
import keyword

def Dashboard(request):
	courses=RegisteredCourse.objects.filter(user=request.user,is_grouped=True)
	qns=Query.objects.filter(raised_by=request.user).count()
	ans=QueryAnswer.objects.filter(answered_by=request.user)
	rewards=len(QueryAnswer.objects.filter(answered_by=request.user).values_list('rewards',flat=True))
	#coursewise
	courseRelated=[]
	for course in courses:
		courseRelated.append({
		"course":{
		"name":course,
		"qns":len(Query.objects.filter(raised_by=request.user,course=course.course)),
		"ans":len(QueryAnswer.objects.filter(answered_by=request.user,question__course=course.course)),
		"rewards":len(QueryAnswer.objects.filter(answered_by=request.user,question__course=course.course).values_list('rewards',flat=True))
		}})
	context={'courses':courses,'qns':qns,'ans':ans.count(),'rewards':rewards,"courseRelated":courseRelated}
	template = loader.get_template('Support/dashboard.html')
	return HttpResponse(template.render(context, request))

#<---------------------------------------------end of dashboard ---------------------------------->


	
def open(request,id):
	
	course=Course.objects.get(id=id)
	grp = CourseGroup.objects.get(user=RegisteredCourse.objects.get(user=request.user,course=course))
	qnss=list(Query.objects.filter(course=course,is_global=False,courseGroup=grp,toUser=None))
	group_mem = grp.user.all()
	globalqns=(list(Query.objects.filter(is_global=True,course=course,toUser=None)))
	qns=qnss+globalqns
	closedqns=[]
	for i in qns:
		if i.is_closed == True:
			closedqns.append(i)
	totalClosedQues=len(closedqns)
	totalUnclosed=len(qns)-len(closedqns)	
	context={"cb":course,"course_grp":id,"qns":qns,"totalClosedQues":totalClosedQues,"totalUnclosed":totalUnclosed,"totalqns":len(qns),'courseid':id,'globalqns':globalqns,"totalglobalqns":len(globalqns),"totallocalqns":len(qnss),"grp":grp,"group_mem":group_mem}
	template = loader.get_template('Support/forum.html')
	return HttpResponse(template.render(context, request))
	
	
		
def questionUpload(request,id):
	course=Course.objects.get(id=id)
	q=Query.objects.create(about = request.POST["about"],raised_by=request.user,query=request.POST['question'],course=course,courseGroup=CourseGroup.objects.get(user=RegisteredCourse.objects.filter(user=request.user,course=course)))
	globalize=request.POST.get('globalize',0)
	if 'globalize' in request.POST:
		q.is_global=True
		q.save()
	question_keywords=q.query.split()
	li=[]
	for key in question_keywords:
		if (key in dir(__builtin__)) or (key in keyword.kwlist):
			print (key)
			li.append({str(key):key})
	q.keywords=li
	q.save()
	return redirect('/open/'+str(id))
	
	
def editQuestion(request,id):
	try:
		qns=get_object_or_404(Query,id=id)
		if request.method=='POST':
			form=EditQuestionForm(request.POST,instance=qns)
			qns.timestamp=datetime.now()
			if form.is_valid():
				form.save()
				return redirect('/quesAnswers/'+str(qns.id))
		else:
			form=EditQuestionForm(instance=qns)
	except Exception as e:
		return HttpResponse(e)
	context={"form":form,"course_grp":qns.course.id}
	return render(request,'Support/editQuestion.html',context)

def quesAnswers(request,id):
	if request.method=='POST':
		QueryAnswer.objects.create(answer=request.POST['answer'],question=Query.objects.get(id=id),answered_by=request.user)	
		return redirect('/quesAnswers/'+str(id))
	else:
		ques=Query.objects.get(id=id)
		answers=ques.queryanswer_set.all()
		context={'answers':answers,'ques':ques,'count':answers.count(),"course_grp":ques.course.id}
		template = loader.get_template('Support/quesAnswers.html')
		return HttpResponse(template.render(context, request))

def editanswer(request,id):
    try:
        ans=get_object_or_404(QueryAnswer,id=id)
        ques=ans.question
        if request.method=='POST':
            form=EditanswerForm(request.POST,instance=ans)
            ans.timestamp=datetime.now()
            if form.is_valid():
                form.save()
                return redirect('/quesAnswers/'+str(ques.id))
        else:
            form=EditanswerForm(instance=ans)
    except Exception as e:
        return HttpResponse(e)
    context={"form":form,"course_grp":ques.course.id,"qnsid":id}
    return render(request,'Support/editanswer.html',context) 

#<-----------------------------------delete answer---------------------------------->

def deleteAnswer(request,id):
	context={'id':id}
	template = loader.get_template('Support/deleteanswer.html')
	return HttpResponse(template.render(context, request))
	
def deleteRedirect(request,id):
	ans=QueryAnswer.objects.get(id=id)
	qns=ans.question
	ans.delete()
	return redirect('/quesAnswers/'+str(qns.id))

#<----------------------------------- end of delete answer---------------------------------->



#<--------------------------------------------search questions------------------------------>
	
def searchQuestions(request):
	li=request.GET.get('kword').split()
	course=Course.objects.get(id=request.GET.get('id'))
	qns=list(Query.objects.filter(reduce(or_, [Q(query__icontains=q) for q in li]),course=course))
	print(qns)
	totalClosedQues=list(Query.objects.filter(reduce(or_, [Q(query__icontains=q) for q in li]),course=course,is_closed=True))

	totalUnclosed=len(qns)-len(totalClosedQues)
	
	context={'qns':qns,'courseid':course.id,"totalClosedQues":len(totalClosedQues),"totalUnclosed":totalUnclosed,"totalqns":len(qns)}
	template = loader.get_template('Support/forum.html')
	return HttpResponse(template.render(context, request))

def keywordSearch(request):
	word=request.GET.get("key")
	course=Course.objects.get(id=request.GET.get('id'))
	qns=list(Query.objects.filter(query__contains=word,course=course))
	totalClosedQues=list(Query.objects.filter(query__contains=word,course=course,is_closed=True))
	totalUnclosed=len(qns)-len(totalClosedQues)
	context={"course_grp":course.id,'qns':qns,'courseid':course.id,"totalClosedQues":len(totalClosedQues),"totalUnclosed":totalUnclosed,"totalqns":len(qns)}
	template = loader.get_template('Support/forum.html')
	return HttpResponse(template.render(context, request))



#<----------------------------------------------end of search questions--------------------->
	
def verify(request):
	ans=QueryAnswer.objects.get(id=request.POST['ansid'])
	ans.rewards=1
	ans.verified_by=Account.objects.get(id=request.user.id)
	ans.save()
	return redirect('/quesAnswers/'+str(ans.question.id))

#<-------------------------------------------close question----------------------------->
def closeQues(request,id):
	qns=Query.objects.get(id=id)
	context={'qns':qns,"course_grp":qns.course.id}
	template = loader.get_template('Support/closeQues.html')
	return HttpResponse(template.render(context, request))
	
def closed(request,id):
	qns=Query.objects.get(id=id)
	course_id=qns.course.id
	qns.is_closed = True
	qns.save()
	return redirect('/open/'+str(course_id)+'/')
#<--------------------------------------end of close qns ------------------------------->
def unClosedQues(request,id):
	course=Course.objects.get(id=id)
	localqns=list(Query.objects.filter(course=course,is_closed=False,is_global=False,courseGroup=CourseGroup.objects.get(user=RegisteredCourse.objects.filter(course=course,user=request.user))).exclude(raised_by=request.user))
	globalqns=list(Query.objects.filter(course=course,is_closed=False,is_global=True))
	totalqns=localqns+globalqns
	context={'totalqns':totalqns,"course_grp":id}
	template = loader.get_template('Support/unClosedQues.html')
	return HttpResponse(template.render(context, request))
#<------------------------------------end of unclosed qns -------------------------------->
def globalize(request,id):
	course=Course.objects.get(id=id)
	qns=list(Query.objects.filter(course=course,raised_by=request.user,is_closed=False))
	context={'qns':qns,"courseid":course.id,"course_grp":id}
	template = loader.get_template('Support/globalizeQues.html')
	return HttpResponse(template.render(context, request))

def globalized(request,id):
	q=Query.objects.get(id=id)
	q.is_global=True
	q.save()
	return redirect('/globalize/'+str(q.course.id)+'/')
#<--------------------------------------------end of globalise qns -------------------------->

################################ a2a ###############################

def A2AQuestionUpload(request,a,b):
	if request.method=='POST':
		courses=Course.objects.get(id=a)
		toUser=Account.objects.get(id=b)
		q=Query.objects.create(about = request.POST["about"],toUser=toUser,raised_by=request.user,query=request.POST['question'],course=courses,courseGroup=CourseGroup.objects.get(user=RegisteredCourse.objects.filter(user=request.user,course=courses)),A2A=True)
		return redirect('/A2AQuestionUpload/'+str(a)+'/'+str(b))
		
	else:	
		course=Course.objects.get(id=a)
		print(b)
		toUser=Account.objects.get(id=b)
		qns=Query.objects.filter(toUser=toUser,raised_by=request.user,A2A=True,course=course)
		template = loader.get_template('Support/A2Aforum.html')
		context={"course_grp":a,'courseid':a,"toUser":toUser.id,'qns':qns}
		return HttpResponse(template.render(context, request))

def ToBeAnswered(request,a):
	qns=Query.objects.filter(toUser=request.user,course=Course.objects.get(id=a))
	template = loader.get_template('Support/ToBeAnswered.html')
	context={'qns':qns,"course_grp":a}
	return HttpResponse(template.render(context, request))

def A2AquesAnswers(request,id):
	qns=Query.objects.get(id=id)
	answers = QueryAnswer.objects.filter(question=qns)
	template = loader.get_template('Support/A2AquesAnswers.html')
	context={"qns":qns,'answers':answers,"course_grp":qns.course.id}
	return HttpResponse(template.render(context, request))

def A2Averify(request):
	ans=QueryAnswer.objects.get(id=request.POST['ansid'])
	ans.rewards=1
	ans.verified_by=Account.objects.get(id=request.user.id)
	ans.save()
	return redirect('/A2AquesAnswers/'+str(ans.question.id))

def A2AoutgoingAnswers(request,id):
	if request.method == 'POST':
		q=Query.objects.get(id=id)
		answer = QueryAnswer.objects.create(question=q,toUser=q.raised_by,answered_by=request.user,answer=request.POST["answer"])
		return redirect('/A2AoutgoingAnswers/'+str(id))
	else:
		qns=Query.objects.get(id=id)
		answers = QueryAnswer.objects.filter(question=qns)
		template = loader.get_template('Support/A2AoutgoingAnswers.html')
		context={"qns":qns,'answers':answers,"course_grp":qns.course.id}
		return HttpResponse(template.render(context, request))
		

