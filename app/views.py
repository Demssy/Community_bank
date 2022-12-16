from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_admins
from .forms import ContactUsForm, UserSetting, ContactAdminForm
from django.http import HttpResponse
from portfolio.models import Project
from blog.models import Blog
from django.contrib import messages
from accounts.form import RegisterUserForm


@login_required
def home(request):
    """
    Home page func
    Get request and retrun home page
    """
    return render(request, 'home.html')

def search(request):
    if request.method =='POST':  
        searched  = request.POST['searched']
        proj = Project.objects.filter(title__contains = searched)
        blog = Blog.objects.filter(title__contains = searched)
        return render(request, 'search.html', {'searched': searched, 'projects':proj, 'blogs':blog})
    else:
         return render(request, 'search.html')


@login_required
def personalArea(request):
    return render(request, 'personalArea.html')

@login_required
def logoutuser(request): #p
    if request.method == 'POST':       #method post!!!
        logout(request)
        return redirect('home')   #return home page after logout

@login_required
def userSettings(request):
    user = get_object_or_404(CustomUser, pk = request.user.id)
    if request.method =='GET':
        form = UserSetting(instance=user)
        return render(request, 'userSettings.html', {'user':user, 'form':form})
    else:
        try:
            form = UserSetting(request.POST, instance=user)
            form.save(user)
            if validator(request.POST['password1'], request.POST['password2']):
                user.set_password(request.POST['password1'])
                user.save()
            return redirect('personalArea')
        except ValueError:
            return render(request, 'userSettings.html', {'user':user, 'form':form, 'error': 'Bad info'}) 

def validator(val1, val2):
    if val1 != '' and val1 == val2:
        return True
    return False    

def SmmaryDataBank(request):
    return render(request,'SmmaryDataBank.html')

def signupuser(request): 
    """
    Sign up func

    """
    # if request.method == "POST":
    #     form = RegisterUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data['username']
    #         password = form.changed_data['password1']
    #         try:
    #             user = authenticate(username= username, password= password)
    #             user.save()
    #             login(request, user)
    #             messages.success(request, ("Registration Successful!"))
    #             return redirect('home')
    #         except IntegrityError : 
    #             return render(request, 'signupuser.html', {'form':RegisterUserForm(), 'error':'That username has already been taken.Please try again'})   
    #     else:
    #         form = RegisterUserForm()    
    #         return render(request, 'signupuser.html', {'form':form})
    # else:
    #     return render(request, 'signupuser.html', {'form':RegisterUserForm()})       




    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form':RegisterUserForm()})  #User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:       #if first and second password equal create new user
            try:
                user = CustomUser.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name = request.POST['first_name'], last_name = request.POST['last_name'],college = request.POST['college'], email = request.POST['email'], major = request.POST['major']) #create user
                user.save()  #save user
                login(request, user)
                messages.success(request, ("Registartion Successful!"))
                return redirect('home')     #return current page
            except IntegrityError : 
                return render(request, 'signupuser.html', {'form':RegisterUserForm(), 'error':'That username has already been taken.Please try again'})
                #if user create login that exist send error massege
        else:  
            return render(request, 'signupuser.html', {'form':RegisterUserForm(), 'error':'Passwords did not match'})      

def loginuser(request):
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

def contactus(request): 
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactus.html')
    else:
        form = ContactUsForm(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form.save()
            form = ContactUsForm()
            form.fields['name'] = ''
            form.fields['email'] = ''
            form.fields['subject'] = ''
            form.fields['message'] = ''
            recipients = ['serj.moskovec@gmail.com']
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            send_mail(subject, message, from_email, recipients)
        else:
            hasError = True
            message = 'Please make sure all fields are valid'
            
    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError })


def contactadmin(request): 
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactadmin.html')
    else:
        form = ContactAdminForm(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form = ContactAdminForm(request.POST)
            form.save()
            # form.fields['subject'] = ''
            # form.fields['message'] = ''
            # subject = request.POST['subject']
            # message = request.POST['message']
            #mail_to_admin = ContactAdmin(subject =subject,message = message)
            #mail_to_admin.save()
            
        else:
            hasError = True
            message = 'Please make sure all fields are valid'
            
    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError })    

