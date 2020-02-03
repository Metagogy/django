from django import forms

from Support.models import * 
class EditanswerForm(forms.ModelForm):
	class Meta:
		model=QueryAnswer
		fields=['answer']

class EditQuestionForm(forms.ModelForm):
	class Meta:
		model=Query
		fields=['query']