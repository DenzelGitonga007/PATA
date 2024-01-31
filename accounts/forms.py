from django.contrib.auth.forms import UserCreationForm # for the user creation
from .models import CustomUser # the model for user creation

# Custom user creation form
class CustomerUserCreationForm(UserCreationForm):
    """Form that creates/registers a user"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
