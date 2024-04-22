from django.contrib import admin
from .models import MissingPerson, Comment, CommentReply

# MissingPerson admin
class MissingPersonAdmin(admin.ModelAdmin):
    """Admin manage the missing person details"""
    list_display = ['user', 'name', 'photo', 'location', 'date_missing', 'created_at', 'display_liked_by']
    search_fields = ['user__username', 'name', 'location', 'date_missing']
    list_filter = ['user', 'name', 'location', 'date_missing']

    def display_liked_by(self, obj):
        return ", ".join([user.username for user in obj.liked_by.all()])

    display_liked_by.short_description = 'Liked by'

admin.site.register(MissingPerson, MissingPersonAdmin)

# Comment admin
class CommentAdmin(admin.ModelAdmin):
    """Admin for managing comments"""
    list_display = ['user', 'post', 'text', 'timestamp']
    search_fields = ['user__username', 'post__name', 'text']
    list_filter = ['post', 'timestamp']

admin.site.register(Comment, CommentAdmin)


# Reply comments

class CommentReplyAdmin(admin.ModelAdmin):
    """Admin to manage comment replies"""
    list_display = ['user', 'comment', 'text', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'comment__text', 'text']
    date_hierarchy = 'timestamp'

admin.site.register(CommentReply, CommentReplyAdmin)

