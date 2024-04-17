from django.contrib import admin
from .models import CustomUser, UserProfile

class CustomUserAdmin(admin.ModelAdmin):
    """Custom user model for the admin site"""
    list_display = ['username', 'email', 'user_type', 'is_superuser']
    list_filter = ['user_type', 'is_superuser']
    search_fields = ['username', 'email', 'user_type', 'is_superuser']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_followers_count', 'get_following_count']
    list_filter = ['user']
    search_fields = ['user']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    get_followers_count.short_description = 'Followers'
    get_following_count.short_description = 'Following'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
