from django import forms
from .models import scolarship

class scolarshipsForm(forms.ModelForm):
    class scolar:
        model = scolarship
        fields = ['title', 'content', 'Location', 'included', 'Amount', 'Hours']



