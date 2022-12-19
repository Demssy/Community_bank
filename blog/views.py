from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm

def SmmaryDataBank(request):
    x={'data':SmmaryDataBank.SmmaryDataBank.all()}
    return render(request,'SmmaryDataBank.html',context=x)


@login_required
def all_blogs(request):
    blogs = Blog.objects.filter(user = request.user).order_by('-date')
    return render(request, 'all_blogs.html', {'blogs':blogs})

@login_required
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    return render(request, 'detail.html', {'blog':blog})      


@login_required
def createBlog(request):
    if request.method == 'GET':
        return render(request, 'createPost.html')
    else:
        try:
            form = BlogForm(request.POST)       #edit form
            newblog = form.save(commit=False)     #save all input data in database
            newblog.user = request.user         
            newblog.save()                        #save data
            return redirect('all_blogs')
        except ValueError:  
            return render(request, 'createPost.html', {'form':BlogForm(), 'error': 'Bad data passed in. Try again'})



@login_required
def editBlog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method =='GET':
        form = BlogForm(instance=blog)
        return render(request, 'editBlog.html', {'blog':blog, 'form':form})
    else:
        try:
            form = BlogForm(request.POST, instance=blog)
            form.save(blog)
            return redirect('detail', blog_id)
        except ValueError:
            return render(request, 'editBlog.html', {'blog':blog, 'form':form, 'error': 'Bad info'}) 
    

@login_required
def deleteBlog(request, blog_id): #delete can do only user who create todo           
    blog = get_object_or_404(Blog, pk = blog_id, user=request.user)   #find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST': #Post becouse we upload data to database
        Blog.delete(blog)                       #delete blog
        return redirect('all_blogs')     #return page with current todos    