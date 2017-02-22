from django.conf.urls import url, include
from django.contrib import admin

from .views import BoardView

urlpatterns = [
	url(r'^(?P<category>\w+)$', BoardView.as_view()),
]
