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

class CreatePostView(FormView):
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
