from django.contrib import admin
from .models import Conversation, Message


# Admin manage chats/conversations
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participants_list', 'last_updated']
    filter_horizontal = ['participants']

    def participants_list(self, obj):
        # Display the list of participants as a comma-separated string
        return ', '.join([str(participant) for participant in obj.participants.all()])
    participants_list.short_description = 'Participants'


    
admin.site.register(Conversation, ConversationAdmin)


# Admin manage messages
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'text', 'timestamp']
    list_filter = ['sender', 'conversation']

admin.site.register(Message, MessageAdmin)