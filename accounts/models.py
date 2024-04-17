from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    """The custom user model"""
    user_type_choices = [
        ('admin', 'Admin'), 
        ('normal_user', 'Normal User')
    ]
    user_type = models.CharField(max_length=12, choices=user_type_choices, default='normal_user')

    def __str__(self):
        return "{}".format(self.username or self.get_full_name())

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followers = models.ManyToManyField(CustomUser, related_name='following_me')
    following = models.ManyToManyField(CustomUser, related_name='following_them')

    def __str__(self):
        return str(self.user)

# Signal to create UserProfile when a CustomUser is created
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
