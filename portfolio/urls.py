from django.urls import include, path
from . import views       


urlpatterns = [                         
    path('', views.userPortfolio, name='userPortfolio'), 
    path('<int:project_id>/', views.detailp, name='detailp'),
    path('create/', views.createPortfolio, name='createPortfolio'),
    path('<int:project_id>/edit', views.editProject, name = 'editProject'),
    path('<int:project_id>/delete', views.deleteProject, name = 'deleteProject'),
    path('projects_page', views.projects_page, name = 'projects_page'),                           #home page path 
]