from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = [
        'user_token'
    ]
    search_fields = ('user_token', )
    list_filter = ('user_token', )
