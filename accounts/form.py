from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    college = forms.CharField(max_length=30)
    major = forms.CharField(max_length=30)
    class Meta:
        model = CustomUser

        fields = ('username', 'first_name', 'last_name', 'email', 'college', 'major', 'password1', 'password2')