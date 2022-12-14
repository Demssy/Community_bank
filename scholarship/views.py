from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Scholarship


def get_all_scholarships(request):
    scholarships = Scholarship.objects.all()

    # scholarships = ['scholarship1','scholarship2','scholarship3']

    return render(request, 'scholarships.html', {'scholarships': scholarships})


def editscolarship(request, scolarship_id):
    scolarship = get_object_or_404(Blog, pk=scolarship_id, user=request.user)
    if request.method == 'GET':
        form = scolarshipsForm(instance=blog)
        return render(request, 'editBlog.html', {'': blog, 'form': form})
    else:
        try:
            form = BlogForm(request.POST, instance=blog)
            form.save(blog)
            return redirect('detail', blog_id)
        except ValueError:
            return render(request, 'editBlog.html', {'blog': blog, 'form': form, 'error': 'Bad info'})





# from django.shortcuts import render
# from django.http import HttpRequest
