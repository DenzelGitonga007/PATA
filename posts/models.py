from django.db import models
from django.contrib.auth import get_user_model # to reference the user model
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

def upload_to(instance, filename):
    return 'missing_persons_photos/{}/{}'.format(instance.user.username, filename)

class MissingPerson(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
    location = models.CharField(max_length=255)
    date_missing = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Field to track users who liked the post
    liked_by = models.ManyToManyField(get_user_model(), related_name='liked_posts')


    def __str__(self):
        return self.name
    

    def toggle_like(self, user):
        """
        Toggle like status for the given user.
        """
        if user in self.liked_by.all():
            self.liked_by.remove(user)
        else:
            self.liked_by.add(user)
            
        self.save()  # Save the instance to update the liked_by field in the database

    def get_absolute_url(self):
        return reverse('posts:view_post_details', kwargs={'post_id': self.pk})





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
