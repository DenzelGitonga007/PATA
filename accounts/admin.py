from django.contrib import admin

# Register your models here.
from .models import CustomUser, UserProfile

# The customuser admin model
class CustomUserAdmin(admin.ModelAdmin):
    """Custom user model for the admin site"""
    list_display = ['username', 'email', 'user_type', 'is_superuser']
    list_filter = ['user_type', 'is_superuser']
    search_fields = ['username', 'email', 'user_type', 'is_superuser']

# User profile
class UserProfileAdmin(admin.ModelAdmin):
    """Admin to manage user profiles"""
    list_display = ['user',]
    list_filter = ['user']
    search_fields = ['user']



admin.site.register(CustomUser, CustomUserAdmin) # register to the site
admin.site.register(UserProfile, UserProfileAdmin) # register the user profile to the admin site