from datetime import datetime

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, FormView, RedirectView

from .forms import LoginForm, JoinForm, ProfileForm
from .models import UserDetail

# Create your views here.
class LoginView(FormView):
	success_url = '/'
	form_class = LoginForm
	template_name = 'account/login_form.html'

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
			return HttpResponseRedirect('/')


class LogoutView(RedirectView):
	url = '/'

	def dispatch(self, request, *args, **kwargs):
		auth.logout(request)
		return super(LogoutView, self).dispatch(request, *args, **kwargs)


class JSONResponseMixin(object):
	def render_to_json_response(self, context, **response_kwargs):
		return JsonResponse(
			self.get_data(context),
			**response_kwargs
		)

	def get_data(self, context):
		return context

class SignupView(JSONResponseMixin, FormView):
	success_url = '/user/login'
	form_class = JoinForm
	template_name = 'account/signup_form.html'

	def render_to_response(self, context):
		if self.request.GET.get('format') == 'json':
			inputID = self.request.GET.get('username_input')
			returnC = {'isExistID': User.objects.filter(username=inputID).exists()}
			return self.render_to_json_response(returnC)
		return super(SignupView, self).render_to_response(context)

	def form_valid(self, form):
		username = form.cleaned_data['id']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		lastname = form.cleaned_data['lastname']
		firstname = form.cleaned_data['firstname']
		user = User.objects.create_user(username=username, password=password, email=email, last_name=lastname, first_name=firstname)
		detail = UserDetail.objects.create(user=user, birthday=datetime.now())
		detail.school = form.cleaned_data['school']
		detail.major = form.cleaned_data['major']
		detail.phone = form.cleaned_data['phone']
		detail.birthday = form.cleaned_data['birthday']
		detail.save()

		return super(SignupView, self).form_valid(form)


class ProfileView(DetailView):
	model = User
	content_object_name = 'user'
	template_name = 'account/profile.html'
	slug_field = 'username'
	slug_url_kwarg = 'username'


class FixProfileView(FormView):
	form_class = ProfileForm
	template_name = 'account/fix_profile.html'

	def get_context_data(self, **kwargs):
		context = super(FixProfileView, self).get_context_data(**kwargs)
		user = User.objects.get(username=self.kwargs['username'])
		context['user'] = user
		if str(self.request.user.username) != str(user.username):
			context['no_auth'] = True
		else:
			context['no_auth'] = False
		return context

	def form_valid(self, form):
		user = User.objects.get(username=self.kwargs['username'])
		detail = UserDetail.objects.filter(user=user)
		user.save()
		if not detail:
			detail = UserDetail(user=user, birthday=datetime.now())
			detail.save()
		else:
			detail = detail.first()
		user.last_name = form.cleaned_data['lastname']
		user.first_name = form.cleaned_data['firstname']
		user.email = form.cleaned_data['email']
		detail.school = form.cleaned_data['school']
		detail.major = form.cleaned_data['major']
		detail.phone = form.cleaned_data['phone']
		detail.birthday = form.cleaned_data['birthday']
		detail.save()
		self.success_url = '/user/' + str(user.username)
		return super(FixProfileView, self).form_valid(form)