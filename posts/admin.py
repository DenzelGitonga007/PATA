from django.contrib import admin
from .models import MissingPerson, Comment, Reaction

# MissingPerson admin
class MissingPersonAdmin(admin.ModelAdmin):
    """Admin manage the missing person details"""
    list_display = ['user', 'name', 'photo', 'location', 'date_missing', 'created_at']
    search_fields = ['user__username', 'name', 'location', 'date_missing']
    list_filter = ['user', 'name', 'location', 'date_missing']

admin.site.register(MissingPerson, MissingPersonAdmin)

# Comment admin
class CommentAdmin(admin.ModelAdmin):
    """Admin for managing comments"""
    list_display = ['user', 'post', 'text', 'timestamp']
    search_fields = ['user__username', 'post__name', 'text']
    list_filter = ['post', 'timestamp']

admin.site.register(Comment, CommentAdmin)

# Reaction admin
class ReactionAdmin(admin.ModelAdmin):
    """Admin for managing reactions"""
    list_display = ['user', 'post', 'type', 'timestamp']
    search_fields = ['user__username', 'post__name']
    list_filter = ['type', 'timestamp']

admin.site.register(Reaction, ReactionAdmin)
