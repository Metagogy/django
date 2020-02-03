# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


import jsonfield
from django.contrib.postgres.fields import ArrayField
from LMS.choices import StatesOfIndia
from Users.models import Account
from .models import * 
import uuid

account_types=(('Employer','Employer'),('mentor','mentor'))

class Course(models.Model):
    name = models.CharField(max_length=200)
    cat = models.CharField(max_length=20)
    author=models.CharField(max_length=200,blank=True, null=True)
    prerequisites=models.TextField(max_length=1000,blank=True, null=True)
    no_of_chapters=models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    duration=models.IntegerField(blank=True, null=True)
    what = models.TextField(max_length=1000)
    why = models.TextField(max_length=1000)
    active = models.BooleanField(default=False)
    workshop = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name+", "+self.cat).encode('ascii', errors='replace')
    
    class Meta:
        verbose_name_plural = 'Course'
    @property
    def sorted_attendee_set(self):
        return self.attendee_set.order_by('last_name')



class Chapter(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=200)
    course=models.ForeignKey(Course,blank=True,null=True,on_delete=models.CASCADE)
    next_chap=models.IntegerField(blank=True,null=True)
    Description=models.TextField(max_length=1000,blank=True,null=True)
    duration=models.FloatField(blank=True,null=True)
    completed_perc=models.FloatField(blank=True,null=True)
    #remove below fields
    timetaken=models.FloatField(blank=True,null=True)
    
    def __str__(self):
        return (self.name + ","+self.course.name).encode('ascii', errors='replace')

class Topic(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=100)
    percentage=models.FloatField(blank=True,null=True)
    Description=models.TextField(max_length=1000, blank=True, null=True)
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,blank=True, null=True)
    notes=models.TextField(max_length=1000, blank=True, null=True)
    page_content = models.CharField(max_length=200,blank=True,null=True)
    video = models.CharField(max_length=200, blank=True, null=True)
    doc = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return (str(self.name)+", "+str(self.chapter.name)).encode('ascii', errors='replace')
    @property

    def sorted_attendee_set(self):
        return self.attendee_set.order_by('last_name')

    class Meta:
        verbose_name_plural = 'Topic'


class Bundle(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    cat = models.CharField(max_length=20)
    price = models.IntegerField(blank=True, null=True)
    duration=models.IntegerField(blank=True, null=True)

    what = models.TextField(max_length=1000)
    why = models.TextField(max_length=1000)
    active = models.BooleanField(default=False)

    def __str__(self):
        return (self.name).encode('ascii', errors='replace')
  
class RegisteredCourse(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True, null=True)
    timetaken=models.FloatField(blank=True,null=True)
    completed_perc=models.FloatField(blank=True,null=True)
    completion_status=models.BooleanField()
    pretest_score=models.FloatField(blank=True,null=True)
    is_grouped=models.BooleanField(default=False)
    def __str__(self):
        return (self.course.name + ","+self.user.username).encode('ascii', errors='replace')

    class Meta:
        verbose_name = 'RegisteredCourse'
        verbose_name_plural = 'RegisteredCourse'
        
class RegisteredBundle(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    bundle=models.ForeignKey(Bundle,on_delete=models.CASCADE,blank=True, null=True)
    timetaken=models.FloatField(blank=True,null=True)
    completed_perc=models.FloatField(blank=True,null=True)
    completion_status=models.BooleanField()
    def __str__(self):
        return (self.bundle.name+","+self.user.username).encode('ascii', errors='replace')

    class Meta:
        verbose_name = 'RegisteredBundle'
        verbose_name_plural = 'RegisteredBundle'


class Cart(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True, null=True)
    bundle=models.ForeignKey(Bundle,on_delete=models.CASCADE,blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return (self.user.username).encode('ascii', errors='replace')

class Test(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic,blank=True, null=True,on_delete=models.CASCADE)
    chapter=models.ForeignKey(Chapter,blank=True, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return (self.name).encode('ascii', errors='replace')

class subTopic(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,blank=True, null=True)
    content = models.TextField(max_length=100,blank=True, null=True)

    def __str__ (self) :
        return (self.name+" in "+ self.topic.name).encode('ascii', errors='replace')


class SubTag(models.Model):
    name = models.CharField(max_length=60)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True, null=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,blank=True, null=True)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    content = models.TextField(max_length=1000000,blank=True, null=True)
    
    def __str__(self):
        return (self.name+","+self.topic.name).encode('ascii', errors='replace')
    
class Question(models.Model):
    question = models.TextField(max_length=300,blank=True, null=True)
    test = models.ForeignKey(Test,blank=True, null=True,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,blank=True, null=True)
    chapter = models.ForeignKey(Chapter,null=True,on_delete=models.CASCADE,blank=True)
    subtopic = models.ForeignKey(subTopic,null=True,blank=True,on_delete=models.CASCADE)
    level_choices = (('Easy','Easy'),('Intermediate','Intermediate'),('Difficult','Difficult'))
    level = models.CharField(choices = level_choices,default='Easy',max_length=100,blank=True, null=True)
    tag = models.ManyToManyField(SubTag,related_name='mcqtag',blank=True, null=True)
    timegiven = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return (self.question).encode('ascii', errors='replace')

class Answer(models.Model):
    ans = models.CharField(max_length=200)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,blank=True,null=True)
    correct=models.BooleanField(default=False)

    def __str__(self):
        return (self.ans).encode('ascii', errors='replace')

class QuizResult(models.Model):
    user = models.ForeignKey(Account,blank=True,null=True,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,blank=True,null=True,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,blank=True,null=True,on_delete=models.CASCADE)
    chapter=models.ForeignKey(Chapter,blank=True,null=True,on_delete=models.CASCADE)
    course=models.ForeignKey(Course, blank=True, null=True,on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    total_time_taken = models.FloatField(default=0.0,blank=True, null=True)
    quiz_percentile = models.FloatField(default=0.0,blank=True, null=True)
    Easy_percentile = models.FloatField(default=0.0,blank=True, null=True)
    Intermediate_percentile = models.FloatField(default=0.0,blank=True, null=True)
    Difficult_percentile = models.FloatField(default=0.0,blank=True, null=True)
    Quiz_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user.username + " , "+str(self.quiz_percentile)).encode('ascii', errors='replace')
      

class Quiz(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    test = models.ForeignKey(Test, blank=True, null=True,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, blank=True, null=True,on_delete=models.CASCADE)
    course=models.ForeignKey(Course, blank=True, null=True,on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    question=models.ForeignKey(Question, blank=True, null=True,on_delete=models.CASCADE)
    ans_submit= models.CharField(max_length=100000)
    corct_ans=models.CharField(max_length=100000)
    iscorrect = models.BooleanField(default=False)
    level_choices=(('Easy','Easy'),('Intermediate','Intermediate'),('Difficult','Difficult'))
    difficulty = models.CharField(choices=level_choices,default='Easy',max_length=100)
    timetaken = models.FloatField(default=0.0,blank=True, null=True)
    Quiz_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__ (self):
        return (str(self.user.username) + " ,  "+str(self.question)+" , "+str(self.timetaken)).encode('ascii', errors='replace')

class employer_task(models.Model):
    course=models.ForeignKey(Course,blank=True, null=True,on_delete=models.CASCADE)
    snippet=models.TextField(max_length=800,blank=True,null=True)
    student=models.ForeignKey(Account,max_length=80,blank=True,null=True,related_name='students',on_delete=models.CASCADE)
    employer=models.ForeignKey(Account,max_length=80,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return unicode(self.student).encode('ascii', errors='replace')

class shortlist(models.Model):
    course=models.ForeignKey(Course,blank=True, null=True,on_delete=models.CASCADE)
    student=models.ForeignKey(Account,max_length=80,blank=True,null=True,related_name='student',on_delete=models.CASCADE)
    employer=models.ForeignKey(Account,max_length=80,blank=True,null=True,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return (self.student.username)

class pretest(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    course = models.ForeignKey(Course,blank=True, null=True,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return unicode(self.name).encode('ascii', errors='replace')

class pretest_questions(models.Model):
    question = models.TextField(max_length=300)
    test = models.ForeignKey(pretest,blank=True, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return (self.question).encode('ascii', errors='replace')

class pretest_answers(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(pretest_questions,on_delete=models.CASCADE,blank=True, null=True)
    correct=models.BooleanField(default=False)
    def __str__(self):
        return unicode(self.answer).encode('ascii', errors='replace')

class pretest_results(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True,on_delete=models.CASCADE)
    test = models.ForeignKey(pretest, blank=True, null=True,on_delete=models.CASCADE)
    question=models.ForeignKey(pretest_questions, blank=True, null=True,on_delete=models.CASCADE)
    submitted_ans= models.CharField(max_length=50)
    correct_ans=models.CharField(max_length=50)
    iscorrect = models.BooleanField(default=False)
    def __str__(self):
        return (self.user.username + " , "+(self.question.question)).encode('ascii', errors='replace')


class Problem(models.Model):
    sl_no=models.IntegerField(blank=True, null=True)
    chapter=models.ForeignKey(Chapter, blank=True, null=True,on_delete=models.CASCADE)
    pblm_id= models.CharField(blank=True, null=True,max_length=100)
    question=models.TextField(max_length=1000,blank=True, null=True)
    level=models.IntegerField(blank=True, null=True)
    instructions=models.TextField(max_length=1000,blank=True, null=True)
    conditions=models.TextField(max_length=1000,blank=True, null=True)
    tags=jsonfield.JSONField(max_length=1000,blank=True, null=True)
    hints=jsonfield.JSONField(max_length=2000,blank=True, null=True)
    subtags=models.ManyToManyField(SubTag,blank=True, null=True)
    timegiven=models.IntegerField(blank=True, null=True)
    note=models.TextField(max_length=1000,blank=True, null=True)
    eg_input=models.TextField(max_length=1000,blank=True, null=True)
    eg_output=models.TextField(max_length=1000,blank=True, null=True)
    testcase1Input = models.TextField(blank=True, null=True)
    testcase1Output = models.TextField(blank=True, null=True)
    testcase2Input = models.TextField(blank=True, null=True)
    testcase2Output = models.TextField(blank=True, null=True)
    testcase3Input = models.TextField(blank=True, null=True)
    testcase3Output = models.TextField(blank=True, null=True)
    rewards = models.IntegerField(default=5)

    def __str__(self):
        return (self.pblm_id).encode('ascii', errors='replace')

class ProbHints(models.Model):
    name= models.CharField(blank=True, null=True,max_length=100)
    problem=models.ForeignKey(Problem, blank=True, null=True,on_delete=models.CASCADE)
    hint=models.TextField(max_length=1000,blank=True, null=True)

    def __str__(self):
        return (self.name).encode('ascii', errors='replace')

# Acts as multi-choices for objective assignments
class TestCases(models.Model):
    sl_no = models.IntegerField(blank=True, null=True)
    problem = models.ForeignKey(Problem, blank=True, null=True,on_delete=models.CASCADE)
    correct_ans = models.TextField(blank=True, null=True)
    testInput = models.TextField()
    testCase = models.TextField()
    ans_choice=jsonfield.JSONField(max_length=1000,blank=True, null=True)
    display = models.BooleanField(default=True)
    def __str__(self):
        return (self.problem.pblm_id).encode('ascii', errors='replace')

class AssignmentResults(models.Model):
    user = models.ForeignKey(Account,blank=True, null=True,on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, blank=True, null=True,on_delete=models.CASCADE)
    problem=models.ForeignKey(Problem,blank=True, null=True)
    ans_records = models.TextField(max_length=10000,blank=True,null=True)
    score = models.FloatField(blank=True,null=True)
    testcase1 = models.BooleanField(default=False)
    testcase2 = models.BooleanField(default=False)
    testcase3 = models.BooleanField(default=False)
    timetaken = models.IntegerField(blank=True, null=True)
    attemps = models.IntegerField(default=0) 
    rewards = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.username + " , "+str(self.score)).encode('ascii', errors='replace')


class Message(models.Model):

     sender = models.ForeignKey(Account,related_name='sender',on_delete=models.CASCADE,blank=True,null=True)
     reciever = models.ForeignKey(Account,related_name='reciever',on_delete=models.CASCADE,blank=True,null=True)
     msg_content = models.TextField(max_length=1000)
     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
     is_read=models.BooleanField(default=False)

     def __str__(self):
        return (self.reciever.username).encode('ascii', errors='replace')
     class Meta:
        ordering = ['-created_at']

class CourseGroup(models.Model):
    name=models.CharField(max_length=200)
    user=models.ManyToManyField(RegisteredCourse)
    course=models.ForeignKey(Course,blank=True,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return (self.name).encode('ascii', errors='replace')
    

class BundleGroup(models.Model):
    name=models.CharField(max_length=200)
    user=models.ManyToManyField(RegisteredBundle)
    bundle=models.ForeignKey(Bundle,blank=True,null=True,on_delete=models.CASCADE)
    

    def __str__(self):
        return (self.name).encode('ascii', errors='replace')
class LastActivity(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course=models.ForeignKey(RegisteredCourse)
    last_url = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return (str(self.user.username)+str(self.course.name)).encode('ascii', errors='replace')
        