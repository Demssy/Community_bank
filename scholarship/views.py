from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Scholarship
from .forms import ScholarshipForm

@login_required
def scholarship(request): #p
    #scholarship = Scholarship.objects.filter(all).order_by('-date')
    return render(request, 'scholarships.html')








