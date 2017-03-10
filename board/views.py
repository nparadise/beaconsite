from datetime import datetime
import html

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView

from .models import Category, Post
from .forms import CheckPasswordForm, CreatePostForm

# Create your views here.
class BoardView(ListView):
	content_object_name = 'post_list'
	template_name = 'board/post_list.html'
	paginate_by = 10

	def get_queryset(self):
		self.category = get_object_or_404(Category, name=self.kwargs['category'])
		return Post.objects.filter(category=self.category).order_by('-register_date')

	def get_context_data(self, **kwargs):
		context = super(BoardView, self).get_context_data(**kwargs)
		context['category'] = self.category
		context['length'] = len(context['post_list'])
		return context


class PostView(DetailView):
	model = Post
	content_object_name = 'post'
	template_name = 'board/post.html'

	def post(self, request, *args, **kwargs):
		pass

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		# set time string output
		date = context['post'].register_date.astimezone()
		hour = date.hour
		if hour >= 12:
			half = '오후 '
			if hour > 13:
				hour -= 12
		else:
			half = '오전 '
			if hour == 0:
				hour = 12
		register_date = str(date.year) + '년 ' + str(date.month) + '월 ' + str(date.day) + '일 ' + half + str(hour) + ':' + str(date.minute) + ':' + str(date.second)
		context['post'].register_date = register_date
		# fix body
		body = html.unescape(context['post'].body)
		context['post'].body = body
		# var to check the owner of the post
		if str(context['post'].author) == str(self.request.user.username):
			context['fixable'] = True
		else:
			context['fixable'] = False
		return context


class CreatePostView(LoginRequiredMixin, FormView):
	login_url = '/user/login'
	form_class = CreatePostForm
	template_name = 'board/create_post.html'

	def get_context_data(self, **kwargs):
		context = super(CreatePostView, self).get_context_data(**kwargs)
		context['category'] = self.kwargs['category']
		return context

	def form_valid(self, form):
		category = Category.objects.get(name=self.kwargs['category'])
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		author = User.objects.get(username=form.cleaned_data['author'])
		post = Post.objects.create_post(category=category, title=title, body=body, author=author)
		self.success_url = '/board/' + str(self.kwargs['category']) + '/' + str(post.id)
		return super(CreatePostView, self).form_valid(form)


class FixPostView(FormView):
	form_class = CreatePostForm
	template_name = 'board/fix_post.html'

	def get_context_data(self, **kwargs):
		context = super(FixPostView, self).get_context_data(**kwargs)
		post = Post.objects.get(id=self.kwargs['pk'])
		if str(self.request.user.username) != str(post.author):
			context['no_auth'] = True
		else:
			context['no_auth'] = False
		context['category'] = post.category
		context['title'] = post.title
		context['body'] = post.body.replace('\r\n', '\\n')
		context['author'] = post.author
		return context

	def form_valid(self, form):
		post = Post.objects.get(id=self.kwargs['pk'])
		post.title = form.cleaned_data['title']
		post.body = form.cleaned_data['body']
		post.modified_date = datetime.now()
		post.save()
		self.success_url = '/board/' + str(post.category) + '/' + str(post.id)
		return super(FixPostView, self).form_valid(form)


class DeletePostView(FormView):
	form_class = CheckPasswordForm
	template_name = 'board/delete_post.html'

	def get_context_data(self, **kwargs):
		context = super(DeletePostView, self).get_context_data(**kwargs)
		post = Post.objects.get(id=self.kwargs['pk'])
		if str(self.request.user.username) != str(post.author):
			context['no_auth'] = True
		else:
			context['no_auth'] = False
		return context

	def form_valid(self, form):
		user = auth.authenticate(username=self.request.user.username, password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				post = Post.objects.filter(id=self.kwargs['pk'])
				if post:
					post.delete()
					self.success_url = '/board/' + self.kwargs['category']
					return super(DeletePostView, self).form_valid(form)
		else:
			return HttpResponseRedirect('/board/' + self.kwargs['category'] + '/' + self.kwargs['pk'])

