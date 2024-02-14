from django.contrib import admin
from . models import MissingPerson

# Register your models here.

class MissingPersonAdmin(admin.ModelAdmin): # MissingPerson model
    """Admin manage the missing person details"""
    list_display = ['user', 'name', 'photo', 'location', 'date_missing', 'created_at']
    search_fields = ['user', 'name', 'photo', 'location', 'date_missing', 'created_at']
    list_filter = ['user', 'name', 'photo', 'location', 'date_missing', 'created_at']

admin.site.register(MissingPerson, MissingPersonAdmin)