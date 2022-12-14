from django.urls import include , path
from . import views  
urlpatterns = [                         
    path('', views.all_blogs, name='all_blogs'),                            #home page path 
    path('<int:blog_id>/', views.detail, name='detail'),
    path('create/', views.createBlog, name='createBlog'),         #create todo
    path('<int:blog_id>/edit', views.editBlog, name = 'editBlog'),
    path('<int:blog_id>/delete', views.deleteBlog, name = 'deleteBlog'),
]