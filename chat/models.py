from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Conversation(models.Model):
    """The Chats model"""
    participants = models.ManyToManyField(User, related_name='conversations')
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ', '.join([str(participant) for participant in self.participants.all()])

    def other_user(self, current_user):
        """
        Returns the other user in the conversation.
        """
        return self.participants.exclude(pk=current_user.pk).first()



# Messages in the chats/conversations
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
