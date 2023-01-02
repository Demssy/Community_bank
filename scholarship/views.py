from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Scholarship
from .forms import ScholarshipForm
from functools import wraps


@login_required
def scholarship(request):
    data = ScholarshipForm()
    data.save()
    return render(request, 'scholarships.html', {'form': form})

def create_schlarship(request):
    form = ScholarshipForm()
    return render(request, 'scholarships.html', {'form': form})

def all_scolarship(request):
    scholarship = scholarship.objects.filter(user = request.user).order_by('-date')
    return render(request, 'scholarships.html', {'scholarship':scholarship})

def admin_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper_func


def create_scholarship(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            return render(request, 'scholarships.html', {'form': form})
    else:
        form = ScholarshipForm()
        return render(request, 'scholarships.html', {'form': form})



def delete_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, pk=scholarship_id)
    scholarship.delete()
    return redirect('success')







