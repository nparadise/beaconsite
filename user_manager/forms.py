from datetime import datetime

from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
	id = forms.CharField(label="ID", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="PASSWORD", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


years = [x for x in range(1900, datetime.now().year + 1)]
months = {1:('1'), 2:('2'), 3:('3'), 4:('4'), 5:('5'), 6:('6'), 7:('7'), 8:('8'), 9:('9'), 10:('10'), 11:('11'), 12:('12')}


class JoinForm(forms.Form):
	id = forms.CharField(label="ID", min_length=5, max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="PASSWORD", min_length=6, max_length=20, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password_check = forms.CharField(label="PASSWORD(again)", min_length=6, max_length=20, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.CharField(label="EMAIL", required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
	firstname = forms.CharField(label="FIRSTNAME", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	school = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	major = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	birthday = forms.DateField(initial=datetime.now(), widget=forms.SelectDateWidget(years=years, months=months, attrs={'class': 'form-control'}))


class ProfileForm(forms.Form):
	email = forms.CharField(label="EMAIL", required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
	firstname = forms.CharField(label="FIRSTNAME", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	school = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	major = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	birthday = forms.DateField(initial=datetime.now(), widget=forms.SelectDateWidget(years=years, months=months, attrs={'class': 'form-control'}))
