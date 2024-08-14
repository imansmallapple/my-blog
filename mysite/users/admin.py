from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import UserProfile

from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)  # unregister user


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.register(User, UserProfileAdmin)