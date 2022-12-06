from django.forms import ModelForm
from .models import Project

class PortfolioForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'url']