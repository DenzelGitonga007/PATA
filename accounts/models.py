from django.db import models

from django.contrib.auth.models import AbstractUser # to customize the user fields

# Create your models here.

# Custom user model
class CustomUser(AbstractUser):
    """The custom user model"""
    user_type_choices = [
        ('admin', 'Admin'), # for the admin
        ('normal_user', 'Normal User') # the normal user
    ]
    user_type = models.CharField(max_length=12, choices=user_type_choices, default='normal_user')
    
    

    def __str__(self):
        return "{}".format(self.username)