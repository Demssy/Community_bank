from django import forms
from .models import Scholarship

#edit scolarship
class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['title', 'content', 'Location', 'requirements', 'Amount', 'Hours', 'image']



