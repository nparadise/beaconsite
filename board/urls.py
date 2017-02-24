from django.conf.urls import url, include
from django.contrib import admin

from .views import BoardView, CreatePostView, PostView

urlpatterns = [
	url(r'^(?P<category>\w+)$', BoardView.as_view()),
	url(r'^(\w+)/(?P<pk>\d+)$', PostView.as_view()),
	url(r'^(?P<category>\w+)/write$', CreatePostView.as_view()),
]
