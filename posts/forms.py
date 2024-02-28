from django import forms
from . models import MissingPerson

# Form the fill the missing person details
class MissingPersonForm(forms.ModelForm):
    """Form to fill the missing person details"""
    class Meta:
        model = MissingPerson
        exclude = ['user','created_at']