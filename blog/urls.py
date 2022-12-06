
from django.urls import include, path
from . import views       


urlpatterns = [                         
    path('', views.all_blogs, name='all_blogs'),                            #home page path 
    path('create/', views.createBlog, name='createBlog'),         #create todo
]