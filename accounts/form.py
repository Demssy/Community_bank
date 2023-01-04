from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget
from .models import CustomUser
from django import forms


class RegisterUserForm(UserCreationForm):
   
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    username = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control','data-toggle': 'password','id': 'password',}))
    college = forms.CharField(max_length=30, required=True)
    major = forms.CharField(max_length=30, required= True)
    date_of_birth = forms.DateField(required=True, widget=SelectDateWidget(years=[y for y in range(1930,2050)]))
    gender = forms.CharField(max_length=10)
    class Meta:
        model = CustomUser

        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'college', 'major', 'password1', 'password2')



 