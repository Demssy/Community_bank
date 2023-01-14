from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_admins
from .forms import ContactUsForm, UserSetting, ContactAdminForm ,DonationsForm, ScholarshipForm
from django.http import HttpResponse
from portfolio.models import Project
from blog.models import Blog
from app import models
from django.contrib import messages
from accounts.form import RegisterUserForm
from .models import SmmaryDataBank
from .models import Scholarship
# from .models import Register
from app import models
from accounts import models as m1
from blog import urls
from django.db.models import Sum


from django.core.exceptions import ValidationError
from blog.forms import BlogForm


def Scholarship(request):
    # scholarship = Scholarship.objects.filter().order_by('title')
    return render(request, 'Scholarship.html', {'scholardata': models.Scholarship.objects.all()})


@login_required
def home(request):
    """
    Home page func
    Get request and return home page
    """
    if request.user.is_investor:
        return render(request,'investorPage.html', status=200)
    else:
        return render(request, 'home.html', status=200)
        

    


@login_required
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        proj = Project.objects.filter(title__contains=searched)
        blog = Blog.objects.filter(title__contains=searched)
        user = CustomUser.objects.filter(username__contains=searched)
        return render(request, 'search.html', {'searched': searched, 'projects': proj, 'blogs': blog, 'users': user}, status=200)
    else:
        return render(request, 'search.html', status=200)


@login_required
def personalArea(request):
    return render(request, 'personalArea.html', status=200)


@login_required
def logoutuser(request):  # p
    if request.method == 'POST':  # method post!!!
        logout(request)
        return redirect('home')  # return home page after logout


@login_required
def userSettings(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'GET':
        form = UserSetting(instance=user)
        return render(request, 'userSettings.html', {'user':user, 'form':form})
    else:
        try:
            form = UserSetting(request.POST, request.FILES, instance=user)
            form.save()
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


def signupuser(request):
    """
    Sign up func

    """

    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': RegisterUserForm()})  # User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:  # if first and second password equal create new user
            try:
                user = CustomUser.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                      first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'],
                                                      college=request.POST['college'],
                                                      date_of_birth=request.POST['date_of_birth'],
                                                      gender=request.POST['gender'], email=request.POST['email'],
                                                      major=request.POST['major'])  # create user
                if request.POST['user_type']:
                    user_type = request.POST['user_type']
                    if user_type == 'student':
                        user.is_student = True
                    elif user_type == 'investor':
                        print('yohohohohohohoho')
                        user.is_investor = True
                    
                user.save()  # save user
                login(request, user)
                messages.success(request, ("Registration Successful!"))

                return redirect('home')
            except ValidationError as e:
                if 'email field must be unique' in e.error_message:
                    return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                               'error': 'That email is already in use. Please try again.'})
                else:
                    return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': e.error_message})
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                           'error': 'That username has already been taken. Please try again.'})
                # if user create login that exist send error massege
        else:
            return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': 'Passwords did not match'})



def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})  # Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username and password did not match')
        elif not user.is_active:
            messages.error(request, 'User is not active')
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')  # return current page
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})


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

    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})


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
            

        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactadmin.html', {'form': form, 'message': message, 'hasError': hasError})

def donations(request): 
    """
    Donations func
    Get request and return donations page
    """
    if request.method == 'GET':
        return render(request, 'donations.html')
    else:
        form = DonationsForm(request.POST)
        message = 'Your donation was sent successfully!! Thanks!!'
        hasError = False
        if form.is_valid():
            form.save()
            form = DonationsForm()
            form.fields['amount'] = ''
            form.fields['scholarship'] = ''
            form.fields['reason'] = ''
            form.fields['email'] = ''
            form.fields['message'] = ''
        else:
            hasError = True
            message = 'Please make sure all fields are valid'
            
    return render(request, 'donations.html', {'form': form, 'message': message, 'hasError': hasError })


def SmmaryDataBank(request):
    if request.method == "GET":
        name = request.GET.get('NameOfFile')
        file = request.GET.get('AddFile')
        data = models.SmmaryDataBank(name=name, file=file)
        data.save()
        return render(request, 'SmmaryDataBank.html')
    return render(request, 'SmmaryDataBank.html', {'data': models.SmmaryDataBank.objects.all()})


@login_required
def all_blogs(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'all_blogs.html', {'blogs': blogs})


@login_required
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    return render(request, 'detail.html', {'blog': blog})


@login_required
def createBlog(request):
    if request.method == 'GET':
        return render(request, 'createPost.html')
    else:
        try:
            form = BlogForm(request.POST)  # edit form
            newblog = form.save(commit=False)  # save all input data in database
            newblog.user = request.user
            newblog.save()  # save data
            return redirect('all_blogs')
        except ValueError:
            return render(request, 'createPost.html', {'form': BlogForm(), 'error': 'Bad data passed in. Try again'})


@login_required
def editBlog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'GET':
        form = BlogForm(instance=blog)
        return render(request, 'editBlog.html', {'blog': blog, 'form': form})
    else:
        try:
            form = BlogForm(request.POST, instance=blog)
            form.save(blog)
            return redirect('detail', blog_id)
        except ValueError:
            return render(request, 'editBlog.html', {'blog': blog, 'form': form, 'error': 'Bad info'})


@login_required
def deleteBlog(request, blog_id):  # delete can do only user who create todo
    blog = get_object_or_404(Blog, pk=blog_id,
                             user=request.user)  # find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST':  # Post becouse we upload data to database
        Blog.delete(blog)  # delete blog
        return redirect('all_blogs')  # return page with current todos
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////


def add_ScholarShip(request,id):
    user = m1.CustomUser.objects.get(id=request.user.id)
    scholar = models.Scholarship.objects.get(id=id)
    user.Scholarship.add(scholar)
    # models.Scholarship.objects.filter(id=id).delete()
    context = {
    'items': models.Scholarship.objects.all(),
    'scholardata': 'Items'}
    print(Scholarship)
    if request.user.is_investor:
        return render(request,'investorPage.html', status=200)
    else:
        return render(request, 'Regester.html',context=context)



@login_required
def reports(request):
    return render(request, 'reports.html')


@login_required
def AddScholarshipINVESOR(request):
    form = ScholarshipForm(request.POST)
    message = 'Message was sent successfully'
    hasError = False
    if form.is_valid():
        form = ScholarshipForm(request.POST)
        form.save()
    return render(request, 'addScholarI.html')




from django.http import JsonResponse

def cancel_scholarship(request):
    user_id = request.POST.get('user_id')
    scholarship_id = request.POST.get('scholarship_id')

    user = CustomUser.objects.get(id=user_id)
    scholarship = Scholarship.objects.get(id=scholarship_id)
    user.Scholarship.remove(scholarship)

    return JsonResponse({'status': 'success'})


def setingUsers(request):
    user = request.user
    scholarships = user.scholarships.all()
    context = {'scholarships': scholarships}
    return render(request, 'template.html', context)

def getScolarship(request, id_scolar):
    scholarship = models.Scholarship.objects.get(id=id_scolar)
    users = scholarship.users.all()
    context = {'users': users}
    return render(request, 'Scholarship.html', context=context)




def selectOption(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            custom_user = form.save()
            if form.cleaned_data['is_student']:
                custom_user.is_student = True
                return render(request, 'home.html', {'form': form})
            elif form.cleaned_data['is_investor']:
                custom_user.is_investor = True
            custom_user.save()
            return render(request, 'investorPageI.html', {'form': form})



def scholarship_detail(request, scholarship_id):
    scholarship = Scholarship.objects.get(id=scholarship_id)
    student_count = scholarship.users.filter(is_student=True).count()
    context = {'scholarship': scholarship, 'student_count': student_count}
    return render(request, 'scholarship_detail.html', context)

from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def scholarship_pdf(request, scholarship_id):
    scholarship = Scholarship.objects.get(id=scholarship_id)
    student_count = scholarship.users.filter(is_student=True).count()
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="scholarship.pdf"'
    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response, pagesize=letter)
    # create a list of tables row
    data = [['Title', scholarship.title],
            ['Content', scholarship.content],
            ['Student Count', student_count],
            ]
    # Create the table
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    # Add the table to the PDF
    p.build([t])
    return response
