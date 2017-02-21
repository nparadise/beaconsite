from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect 
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from .forms import LoginForm, JoinForm

# Create your views here.
class LoginView(FormView):
	success_url = '/'
	form_class = LoginForm
	template_name = 'user_manager/login_form.html'

	@method_decorator(sensitive_post_parameters('password'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = auth.authenticate(username=form.cleaned_data['id'], password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				auth.login(self.request, user)
				return super(LoginView, self).form_valid(form)
		else:
			print("no")
			return HttpResponseRedirect('/')


class LogoutView(RedirectView):
	url = '/'

	def dispatch(self, request, *args, **kwargs):
		auth.logout(request)
		return super(LogoutView, self).dispatch(request, *args, **kwargs)


class SignupView(FormView):
	success_url = '/user/login'
	form_class = JoinForm
	template_name = 'user_manager/signup_form.html'

	def form_valid(self, form):
		username = form.cleaned_data['id']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		User.objects.create_user(username=username, password=password, email=email)

		return super(SignupView, self).form_valid(form)