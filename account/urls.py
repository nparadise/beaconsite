from django.conf.urls import url
from django.contrib import admin

from .views import FixProfileView, LoginView, LogoutView, ProfileView, SignupView

urlpatterns = [
    url(r'^login$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^signup$', SignupView.as_view()),
    url(r'^(?P<username>[\w-]+)$', ProfileView.as_view()),
    url(r'^(?P<username>[\w-]+)/fix$', FixProfileView.as_view()),
]