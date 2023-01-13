from django.forms import ModelForm
from .models import Project
from django import forms

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'url', 'project_type']
        widgets = {
            'project_type': forms.Select()
        }