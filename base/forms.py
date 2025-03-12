from django import forms
from base.models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control fsz-12px rounded-0 p-3',
                'placeholder': 'Your Name *'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded-0 fsz-12px p-3',
                'placeholder': 'Write your comment here',
                'rows': 6
            }),
            'parent': forms.HiddenInput(),
        }
