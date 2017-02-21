from django.conf.urls import url
from django.contrib import admin

from .views import LoginView, LogoutView, SignupView

urlpatterns = [
    url(r'^login$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^signup$', SignupView.as_view()),
]