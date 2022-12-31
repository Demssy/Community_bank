from django.urls import path
from . import views

urlpatterns = [                         
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('create/', views.createBlog, name='createBlog'),
    path('<int:blog_id>/edit', views.editBlog, name = 'editBlog'),
    path('<int:blog_id>/delete', views.deleteBlog, name = 'deleteBlog'),
    path('blogs_page', views.blogs_page, name = 'blogs_page'),
]