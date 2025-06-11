from django import forms
from django.forms import ModelForm
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a desc.' }),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
