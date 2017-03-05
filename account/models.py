from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserDetail(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	school = models.CharField(max_length=30, blank=True)
	major = models.CharField(max_length=30, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	birthday = models.DateField()

	def __str__(self):
		return str(self.user)
