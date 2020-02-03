from django import forms
from Users.models import Account
class UploadFileForm(forms.Form):
    
    file = forms.FileField()
class EmpForm(forms.ModelForm):
	class Meta:
		model=Account
		fields=['first_name','last_name','username','address','phone_number','account_type','email','organisation','position','password']
class mentorUpdateForm(forms.ModelForm):
	class Meta:
		model=Account
		fields=['address','phone_number','experience','technologies']
class empUpdateForm(forms.ModelForm):
	class Meta:
		model=Account
		fields=['address','phone_number','organisation','position']