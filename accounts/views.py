from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from blog.models import Blog
from portfolio.models import Project
from django.contrib.auth.decorators import login_required



@login_required
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    blogs = Blog.objects.filter(user = user).order_by('-date')
    projects = Project.objects.filter(user = user)
    return render(request, 'user_profile.html', {'requested_user':user, 'blogs':blogs, 'projects':projects, 'user':request.user})
    