from django.db import models
from django.contrib.auth import get_user_model # to reference the user model
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings


# Create your models here.


# File name path
def upload_to(instance, filename):
    """Uploading the image to the path of username"""
    return 'missing_persons_photos/{}/{}'.format(instance.user.username, filename)


class MissingPerson(models.Model): # the missing persons details
    """The missing person model"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(
        upload_to=upload_to, # upload path
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            
            ]
        )
    location = models.CharField(max_length=255)
    date_missing = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Stringify
    def __str__(self):
        """Stringify the name"""
        return self.name
    

# Comments
class Comment(models.Model):
    """Comments model"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(MissingPerson, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return "Comment by {} on {}".format((self.user.username), (self.timestamp))


# Reply to comments   
class CommentReply(models.Model):
    """Model to store replies to comments"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Reply by {} on {} to comment by {}".format(self.user.username, self.timestamp, self.comment.user.username)

# Reactions
class Reaction(models.Model):
    """Reactions model"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(MissingPerson, on_delete=models.CASCADE)
    type_choices = [
        ('sympathize', 'Sympathize'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} by {} on {}".format(self.get_type_display(), self.user.username, self.timestamp)
