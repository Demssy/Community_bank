from django import forms
from django.forms import TextInput
from .models import ContactUsModel, ContactAdmin, DonationsModel, DonationsModel
from accounts.models import CustomUser

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ["name", "email", "subject", "message"]

class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = ContactAdmin
        fields = ["subject", "message"]

class UserSetting(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['major', 'college', 'first_name', 'last_name', 'email', 'user_avatar', 'date_of_birth', 'gender', 'bio']
        widgets = {'date_of_birth':forms.DateInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              })}

class DonationsForm(forms.ModelForm):
    class Meta:
        model = DonationsModel
        fields = ["amount", "scholarship", "reason", "email", "message"]


