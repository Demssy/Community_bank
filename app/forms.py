from django import forms
from django.forms import TextInput
from .models import ContactUsModel, ContactAdmin
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
        fields = ['major', 'college', 'first_name', 'last_name', 'email']
        # widgets={
        # 'password1':TextInput(attrs={'type':'password'})
        # }
