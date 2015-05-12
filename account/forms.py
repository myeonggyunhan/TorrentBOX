from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account 

class TorrentBoxCreateForm(UserCreationForm):
	username = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'placeholder': 'Email address', 'class':'form-control', 'required': 'true', 'autofocus': 'true'}))
	password1 = forms.CharField(min_length=3, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control', 'required': 'true'}))
	password2 = forms.CharField(min_length=3, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password confirm', 'class':'form-control', 'required': 'true'}))

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def save(self, commit=True):
		user = super(TorrentBoxCreateForm, self).save(commit=False)
		user.save()
		user_profile = Account(user=user)

		if commit:
			user_profile.save()

		return user_profile


class TorrentBoxAuthForm(AuthenticationForm):
	username = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'placeholder': 'Email address', 'class':'form-control', 'required': 'true', 'autofocus':'true'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control', 'required': 'true'}))

	def is_value(self):
		form = super(TorrentBoxAuthForm, self).is_valid()

		return form
