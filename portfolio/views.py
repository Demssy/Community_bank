from django.shortcuts import redirect, render, get_object_or_404
from portfolio.models import Project
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm


@login_required
def userPortfolio(request): #p
    projects=Project.objects.filter(user = request.user)
    return render(request, 'userPortfolio.html', {'projects':projects})   

@login_required
def projects_page(request):
    projects = Project.objects.order_by('title')
    return render(request,'projects_page.html', {'projects':projects})

@login_required
def detailp(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.project_type_name = project.get_project_type_name(project.project_type)
    return render(request, 'detailp.html', {'project':project}) 

@login_required
def createPortfolio(request):
    if request.method == 'GET':
        form = PortfolioForm()
        return render(request, 'createPortfolio.html', {'form': form})
    else:
        try:
            form = PortfolioForm(request.POST, request.FILES)       #edit form
            newPortfolio = form.save(commit=False)     #save all input data in database
            newPortfolio.user = request.user         
            newPortfolio.save()                        #save data
            return redirect('userPortfolio')
        except ValueError:  
            return render(request, 'createPortfolio.html', {'form':PortfolioForm(), 'error': 'Bad data passed in. Try again'})



@login_required
def editProject(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    if request.method =='GET':
        form = PortfolioForm(instance=project)
        return render(request, 'editProject.html', {'project':project, 'form':form})
    else:
        try:
            form = PortfolioForm(request.POST, request.FILES, instance=project)
            form.save(project)
            return redirect('detailp', project_id)
        except ValueError:
            return render(request, 'editProject.html', {'project':project, 'form':form, 'error': 'Bad info'}) 
    

@login_required
def deleteProject(request, project_id): #delete can do only user who create todo           
    project = get_object_or_404(Project, pk = project_id, user=request.user)   #find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST': #Post becouse we upload data to database
        Project.delete(project)                       #delete blog
        return redirect('userPortfolio')     #return page with current todos    