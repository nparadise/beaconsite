from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
	id = forms.CharField(label="ID", max_length=12)
	password = forms.CharField(label="PASSWORD", max_length=20, widget=forms.PasswordInput)


class JoinForm(forms.Form):
	id = forms.CharField(label="ID", min_length=5, max_length=12, required=True)
	password = forms.CharField(label="PASSWORD", min_length=6, max_length=20, required=True, widget=forms.PasswordInput)
	password_check = forms.CharField(label="PASSWORD(again)", min_length=6, max_length=20, required=True, widget=forms.PasswordInput)
	email = forms.CharField(label="EMAIL", required=False,widget=forms.EmailInput)