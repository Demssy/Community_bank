from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget
from .models import CustomUser
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class RegisterUserForm(forms.ModelForm):
   
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    username = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control','data-toggle': 'password','id': 'password',}))
    college = forms.CharField(max_length=30, required=False)
    major = forms.CharField(max_length=30, required= False)
    date_of_birth = forms.DateField(required=True, widget=SelectDateWidget(years=[y for y in range(1930,2050)]))
    gender = forms.CharField(max_length=10)
    is_student = forms.BooleanField(required=False)
    is_investor = forms.BooleanField(required=False)
    class Meta:
        model = CustomUser

        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'college', 'major', 'password1', 'password2', 'is_student', 'is_investor')


    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already in use')
            return email    

    def clean(self):
        cleaned_data = super().clean()
        if 'email' in cleaned_data:  
            email = cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                self.add_error('email', 'This email is already in use')
        if 'password1' in cleaned_data and 'password2' in cleaned_data:
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Passwords do not match')