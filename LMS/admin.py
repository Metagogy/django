# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Bundle)

admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(RegisteredCourse)
admin.site.register(RegisteredBundle)

admin.site.register(Question)
admin.site.register(SubTag)
admin.site.register(Answer)

admin.site.register(Test)
#admin.site.register(User)
admin.site.register(CourseGroup)
admin.site.register(BundleGroup)

admin.site.register(Message)
admin.site.register(AssignmentResults)
admin.site.register(Cart)
# admin.site.register(Project)
# admin.site.register(project_chapters)

admin.site.register(shortlist)
admin.site.register(employer_task)
admin.site.register(pretest)
admin.site.register(pretest_questions)
admin.site.register(pretest_answers)
admin.site.register(pretest_results)
admin.site.register(Quiz)
# admin.site.register(TopicQuizResult)
admin.site.register(subTopic)
admin.site.register(Problem)
admin.site.register(ProbHints)
admin.site.register(TestCases)
admin.site.register(QuizResult)
admin.site.register(LastActivity)
