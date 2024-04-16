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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followers = models.ManyToManyField(CustomUser, related_name='following_me')
    following = models.ManyToManyField(CustomUser, related_name='following_them')

    def __str__(self):
        return str(self.user)
