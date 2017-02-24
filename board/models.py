from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=30)

	class Meta:
		permissions = (
			('can_ notice', 'Can write notice'),
		)

	def __str__(self):
		return self.name

class PostManager(models.Manager):
	def create_post(self, category, title, body, author):
		post = self.create(category=category, title=title, body=body, author=author)
		return post

class Post(models.Model):
	category = models.ForeignKey(Category, null = True)
	title = models.CharField(max_length=100)
	body = models.TextField()
	author = models.ForeignKey(User)
	register_date = models.DateTimeField(auto_created=True, auto_now_add=True)
	modified_date = models.DateTimeField(auto_created=True, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
		return str(self.category) + ' / ' + str(self.title) + ' / ' + str(self.author)