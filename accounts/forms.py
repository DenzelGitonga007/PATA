from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # for the user creation and login/authentication
from .models import CustomUser # the model for user creation
from django import forms

# Custom user creation form
class CustomerUserCreationForm(UserCreationForm):
    """Form that creates/registers a user"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # the password fields are pulled from the parent class, UserCreationForm
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if password1 and password2 match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")


# Custom authentication/login form
class CustomUserAuthenticationForm(AuthenticationForm):
    """Form for login/authentication"""
    class Meta:
        model = CustomUser
        fields = ['username']
