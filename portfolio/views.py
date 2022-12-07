from django.shortcuts import redirect, render
from portfolio.models import Project
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm


@login_required
def userPortfolio(request): #p
    projects=Project.objects.filter(user = request.user)
    return render(request, 'userPortfolio.html', {'projects':projects})   



@login_required
def createPortfolio(request):
    if request.method == 'GET':
        return render(request, 'createPortfolio.html', {'form':PortfolioForm()})
    else:
        try:
            form = PortfolioForm(request.POST, request.FILES)       #edit form
            newPortfolio = form.save(commit=False)     #save all input data in database
            newPortfolio.user = request.user         
            newPortfolio.save()                        #save data
            return redirect('userPortfolio')
        except ValueError:  
            return render(request, 'createPortfolio.html', {'form':PortfolioForm(), 'error': 'Bad data passed in. Try again'})
