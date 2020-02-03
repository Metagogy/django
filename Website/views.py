# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.template import loader

# Create your views here.
def internships(request):
    template=loader.get_template('Website/internships.html')
    context={}
    return HttpResponse(template.render(context,request))

def about(request):
	template=loader.get_template('Website/about.html')
	context={}
	return HttpResponse(template.render(context,request))

def tech(request):
	template=loader.get_template('Website/blog.html')
	context={}
	return HttpResponse(template.render(context,request))

def events(request):
	template=loader.get_template('Website/events.html')
	context={}
	return HttpResponse(template.render(context,request))

def contact(request):
	template=loader.get_template('Website/contact.html')
	context={}
	return HttpResponse(template.render(context,request))