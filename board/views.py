from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView

from .models import Category, Post
from .forms import CreatePostForm

# Create your views here.
class BoardView(ListView):
	content_object_name = 'post_list'
	template_name = 'board/post_list.html'
	paginate_by = 5

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

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
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
		context['body'] = post.body
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