from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# from .forms import TodoForm
# from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def home(request): #p
    """
    Home page func
    Get request and retrun home page
    """
    return render(request, 'todo/home.html')



def signupuser(request): #p
    """
    Sign up func

    """
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})  #User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:       #if first and second password equal create new user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) #create user
                user.save()  #save user
                login(request, user)
                return redirect('currenttodos')     #return current page
            except IntegrityError : 
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken.Please try again'})
                #if user create login that exist send error massege
        else:  
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})
            #if user made mistake in entering second password

def loginuser(request):#p
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()}) #Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
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

# @login_required
# def createtodo(request):
#     if request.method == 'GET':
#         return render(request, 'todo/createtodo.html', {'form':TodoForm()})
#     else:
#         try:
#             form = TodoForm(request.POST)       #edit form
#             newtodo = form.save(commit=False)     #save all input data in database
#             newtodo.user = request.user         
#             newtodo.save()                        #save data
#             return redirect('currenttodos')
#         except ValueError:  
#             return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error': 'Bad data passed in. Try again'})


# @login_required
# def currenttodos(request):#p           1                        2
#     todos = Todo.objects.filter(user = request.user, datecompleted__isnull=True)   #1 just users who create task can see him 2 if task completed(set date of completed task) its disapears from the list//display tasks that not completed
#     return render(request, 'todo/currenttodos.html', {'todos': todos})

# @login_required
# def completedtodos(request):#p           1                        2            filter that display comleted task in rever chronological order(order_by('-datecompleted'))
#     todos = Todo.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')   #1 just users who create task can see him 2 if task completed(set date of completed task) its disapears from the list//display completed tasks
#     return render(request, 'todo/completedtodos.html', {'todos': todos})                  


# @login_required
# def viewtodo(request, todo_pk):        
#     todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)   #find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
#     if request.method == 'GET':
#         form = TodoForm(instance=todo)                #displaying form with option to edit it (instance=todo)- to work with existed form
#         return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})  #return page with specific todo
#     else:  
#         try:  
#             form = TodoForm(request.POST, instance=todo)       #edit form
#             form.save()                         #save form
#             return redirect('currenttodos')     #return page with current todos
#         except ValueError:  
#             return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})  #return page with specific todo and display 'error'

# @login_required
# def completetodo(request, todo_pk): #complete can do only user who create todo           
#     todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)   #find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
#     if request.method == 'POST': #Post becouse we upload data to database
#         todo.datecompleted=timezone.now() #check if task completed
#         todo.save()                       #save changes
#         return redirect('currenttodos')     #return page with current todos



# @login_required
# def deletetodo(request, todo_pk): #delete can do only user who create todo           
#     todo = get_object_or_404(Todo, pk = todo_pk, user=request.user)   #find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
#     if request.method == 'POST': #Post becouse we upload data to database
#         todo.delete()                       #delete todo
#         return redirect('currenttodos')     #return page with current todos


