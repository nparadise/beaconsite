from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserDetail(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	school = models.CharField(max_length=30)
	major = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	birthday = models.DateField()

	def __str__(self):
		return str(self.user)