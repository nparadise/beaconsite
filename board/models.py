from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Post(models.Model):
	category = models.ForeignKey(Category, null = True)
	title = models.CharField(max_length=100)
	body = models.TextField()
	author = models.ForeignKey(User)
	register_date = models.DateTimeField(auto_created=True, auto_now_add=True)
	modified_date = models.DateTimeField(auto_created=True, auto_now_add=True)

	def __str__(self):
		return str(self.category) + ' / ' + str(self.title) + ' / ' + str(self.author)