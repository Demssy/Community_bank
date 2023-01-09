from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from blog.models import Blog
from portfolio.models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages



@login_required
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    blogs = Blog.objects.filter(user = user).order_by('-date')
    projects = Project.objects.filter(user = user)
    return render(request, 'user_profile.html', {'requested_user':user, 'blogs':blogs, 'projects':projects, 'user':request.user})


def index(request):
    return None
#
#
# def afterlogin_view(request):
#     """after login for users """
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_staff:
#                     auth.login(request, user)
#                     return redirect('AdminPage')
#                 if user is not None and user.groups.filter(name='investor').exists():
#                     auth.login(request, user)
#                     return redirect('investor')
#                 if user is not None and user.groups.filter(name='customer').exists():
#                     print("asdasdas")
#                     auth.login(request, user)
#                     return redirect('home')
#                 return None
#             else:
#                 messages.info(request, 'invalid username or password')
#                 return redirect('login')
#         else:
#             return render(request, 'AdminPage.html')
#     else:
#         if request.user.is_staff:
#             return redirect('admin')
#         if request.user.groups.filter(name='investor'):
#             return redirect('investor')
#         if request.user.groups.filter(name='customer'):
#             return redirect('home')
#     return None
#
#
# def investor(request):
#     return render(request,'InvestorHome.html')
#
# def admin(request):
#     return render(request,'AdminPage.html')
#
# def customer(request):
#     return render(request,'home.html')