from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # Add 'date_joined' and 'last_login' to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_user', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_user', 'is_superuser', 'is_active', 'groups', 'date_joined', 'last_login')


admin.site.register(User, CustomUserAdmin)
