# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from LMS.models import *
from Users.models import *
# Create your models here.
class Query(models.Model):
	about = models.TextField(max_length=1000,blank=True,null=True)
	query=models.TextField(max_length=100000,blank=True,null=True)
	raised_by=models.ForeignKey(Account,blank=True,null=True,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,blank=True,null=True,on_delete=models.CASCADE)
	timestamp=models.DateTimeField(auto_now_add=True, blank=True, null=True)
	courseGroup=models.ForeignKey(CourseGroup,related_name="courseGroup",blank=True,null=True,on_delete=models.CASCADE)
	toUser= models.ForeignKey(Account,blank=True,null=True,related_name='tuser',on_delete=models.CASCADE)
	keywords=jsonfield.JSONField()
	A2A=models.BooleanField(default=False)
	is_global=models.BooleanField(default=False)
	is_closed=models.BooleanField(default=False)
	is_read = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.query

class QueryAnswer(models.Model):
	answer=models.TextField(max_length=1000,blank=True,null=True)
	answered_by=models.ForeignKey(Account,blank=True,null=True,related_name='user',on_delete=models.CASCADE)
	question=models.ForeignKey(Query,blank=True,null=True,on_delete=models.CASCADE)
	timestamp=models.DateTimeField(auto_now_add=True, blank=True, null=True)
	rewards=models.IntegerField(default=0)
	toUser= models.ForeignKey(Account,blank=True,null=True,related_name='touser',on_delete=models.CASCADE)
	verified_by=models.ForeignKey(Account,blank=True,null=True,related_name='mentor',on_delete=models.CASCADE)	
	def __unicode__(self):
		return self.answer