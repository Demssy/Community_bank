from django.urls import include, path
from . import views       


urlpatterns = [                         
    path('', views.userPortfolio, name='userPortfolio'), 
    path('create/', views.createPortfolio, name='createPortfolio'),                           #home page path 
]