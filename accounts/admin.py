from django.contrib import admin

# Register your models here.
from .models import CustomUser

# The customuser admin model
class CustomUserAdmin(admin.ModelAdmin):
    """Custom user model for the admin site"""
    list_display = ['username', 'email', 'user_type', 'is_superuser']
    list_filter = ['user_type', 'is_superuser']
    search_fields = ['username', 'email', 'user_type', 'is_superuser']

admin.site.register(CustomUser, CustomUserAdmin) # register to the site
