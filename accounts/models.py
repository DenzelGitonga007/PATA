from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """The custom user model"""
    user_type_choices = [
        ('admin', 'Admin'), 
        ('normal_user', 'Normal User')
    ]
    user_type = models.CharField(max_length=12, choices=user_type_choices, default='normal_user')
    profile = models.OneToOneField('accounts.UserProfile', related_name='user_profile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.username or self.get_full_name())

class UserProfile(models.Model):
    """The User's profile, with followers"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followers = models.ManyToManyField(CustomUser, related_name='following')

    def __str__(self):
        return str(self.user)
    
    def follow(self, user):
        """
        Method to follow another user
        """
        self.followers.add(user)

    def unfollow(self, user):
        """
        Method to unfollow another user
        """
        self.followers.remove(user)

    def is_following(self, user):
        """
        Method to check if the user is following another user
        """
        return self.followers.filter(pk=user.pk).exists()
