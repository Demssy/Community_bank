from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from .models import Blog
from .forms import BlogForm

@login_required
def all_blogs(request):
    blogs = Blog.objects.filter(user = request.user).order_by('-date')[:5]
    return render(request, 'all_blogs.html', {'blogs':blogs})


@login_required
def createBlog(request):
    if request.method == 'GET':
        return render(request, 'createPost.html', {'form':BlogForm()})
    else:
        try:
            form = BlogForm(request.POST)       #edit form
            newblog = form.save(commit=False)     #save all input data in database
            newblog.user = request.user         
            newblog.save()                        #save data
            return redirect('all_blogs')
        except ValueError:  
            return render(request, 'createPost.html', {'form':BlogForm(), 'error': 'Bad data passed in. Try again'})