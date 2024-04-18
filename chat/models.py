from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model() # the user from accounts app

class Conversation(models.Model):
    """The Chats model"""
    # Many-to-many relationship with users to store participants of the conversation
    participants = models.ManyToManyField(User, related_name='conversations')
    
    # Timestamp to track when the conversation was last updated
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Display the participants' usernames as the representation of the conversation
        return ', '.join([str(participant) for participant in self.participants.all()])

class Message(models.Model):
    """The messages in the chats"""
    # Foreign key to link messages to their respective conversations
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    # Foreign key to indicate the user who sent the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Text content of the message
    text = models.TextField()
    
    # Timestamp to track when the message was sent
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Display the sender's username and the message content
        return f'{self.sender}: {self.text}'
