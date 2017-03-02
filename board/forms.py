from django import forms
from django.contrib import auth


class CreatePostForm(forms.Form):
	category = forms.CharField(label="category", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	title = forms.CharField(label="title", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	body = forms.CharField(label="body", widget=forms.Textarea(attrs={'class': 'form-control'}))
	author = forms.CharField(label="author", max_length=12,  widget=forms.TextInput(attrs={'class': 'form-control'}))