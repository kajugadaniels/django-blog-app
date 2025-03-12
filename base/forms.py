from django import forms
from base.models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control fsz-12px rounded-0 p-3',
                'placeholder': 'Your Name *'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded-0 fsz-12px p-3',
                'rows': 6,
                'placeholder': 'Write your comment here'
            }),
        }
