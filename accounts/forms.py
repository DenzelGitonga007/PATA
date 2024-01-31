from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # for the user creation and login/authentication
from .models import CustomUser # the model for user creation

# Custom user creation form
class CustomerUserCreationForm(UserCreationForm):
    """Form that creates/registers a user"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email'] # the password fields are pulled from the parent class, UserCreationForm
    
# Custom authentication/login form
class CustomUserAuthenticationForm(AuthenticationForm):
    """Form for login/authentication"""
    class Meta:
        model = CustomUser
        fields = ['username']
