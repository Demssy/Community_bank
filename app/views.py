from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from portfolio.models import Project

from .forms import ContactUsForm

@login_required
def home(request): #p
    """
    Home page func
    Get request and retrun home page
    """
    return render(request, 'app/home.html')

def SmmaryDataBank(request):
    return render(request,'app/SmmaryDataBank.html')
@login_required
def PersonalArea(request): #p
    return render(request, 'app/PersonalArea.html')


def signupuser(request): #p
    """
    Sign up func

    """
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form':UserCreationForm()})  #User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:       #if first and second password equal create new user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) #create user
                user.save()  #save user
                login(request, user)
                return redirect('home')     #return current page
            except IntegrityError : 
                return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken.Please try again'})
                #if user create login that exist send error massege
        else:  
            return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})
            #if user made mistake in entering second password

def loginuser(request):#p
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()}) #Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home') #return current page    

@login_required
def logoutuser(request): #p
    if request.method == 'POST':       #method post!!!
        logout(request)
        return redirect('home')   #return home page after logout


def contactus(request): #p
    """
    Contact US func
    Get request and retrun contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactus.html')
    else:
        form = ContactUsForm(request.POST)
        message = 'Message was sent successfuly'
        hasError = False
        if form.is_valid():
            form.save()
            form = ContactUsForm()
            form.fields['name'] = ''
            form.fields['email'] = ''
            form.fields['subject'] = ''
            form.fields['message'] = ''
        else:
            hasError = True
            message = 'Please make sure all field are valid'
            
    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError })

def hintTemplate(key, errors):
    return key.capitalize() + ' ' + errors[key]



