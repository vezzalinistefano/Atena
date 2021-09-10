from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.forms import RegisterForm
from users.forms import UserProfileForm
from users.models import UserProfile


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = UserProfileForm
    model = UserProfile
    list_filter = ('is_teacher',)
    fieldsets = (
        (None,
         {'fields': ('email', 'password', 'is_teacher', 'username', 'user_photo', 'first_name', 'last_name', 'bio',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'username', 'first_name', 'last_name', 'user_photo', 'password1', 'password2', 'is_teacher',
            'bio',)}
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.register(UserProfile, CustomUserAdmin)
