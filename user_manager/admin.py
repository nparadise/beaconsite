from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserDetail
# Register your models here.

class UserDetailInline(admin.StackedInline):
	model = UserDetail
	can_delete = False
	verbose_name_plural = 'UserDetails'

class UserAdmin(BaseUserAdmin):
	inlines = (UserDetailInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)