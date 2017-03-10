from django import forms
from django.contrib import auth


class CreatePostForm(forms.Form):
	category = forms.CharField(label="category", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	title = forms.CharField(label="title", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	body = forms.CharField(label="body", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '20'}))
	author = forms.CharField(label="author", max_length=12,  widget=forms.TextInput(attrs={'class': 'form-control'}))


class CheckPasswordForm(forms.Form):
	password = forms.CharField(label="password", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
