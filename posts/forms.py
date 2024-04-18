from django import forms
from . models import CommentReply, MissingPerson, Comment, Reaction

# Form the fill the missing person details
class MissingPersonForm(forms.ModelForm):
    """Form to fill the missing person details"""
    class Meta:
        model = MissingPerson
        exclude = ['user','created_at']
        widgets = {
            'date_missing': forms.DateInput(attrs={'time': 'date'}),
        }


# Form for creating a comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

# Comment reply
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']        

# Form for creating a reaction
class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['type']
