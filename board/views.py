from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Category, Post

# Create your views here.
class BoardView(ListView):
	# queryset = Post.objects.filter(category=Category.objects.get(name='공지사항'))
	content_object_name = 'post_list'
	template_name = 'board/post_list.html'
	paginate_by = 5

	def get_queryset(self):
		self.category = get_object_or_404(Category, name=self.kwargs['category'])
		return Post.objects.filter(category=self.category)

	def get_context_data(self, **kwargs):
		context = super(BoardView, self).get_context_data(**kwargs)
		context['category'] = self.category
		context['length'] = len(context['post_list'])
		return context