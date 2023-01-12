from django.urls import path
from . import views
from app import views as appviews
from accounts import urls
urlpatterns = [
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('create/', views.createBlog, name='createBlog'),
    path('<int:blog_id>/edit', views.editBlog, name = 'editBlog'),
    path('<int:blog_id>/delete', views.deleteBlog, name = 'deleteBlog'),
    path('blogs_page', views.blogs_page, name = 'blogs_page'),
    path('SmmaryDataBank/', appviews.SmmaryDataBank, name='SmmaryDataBank'),
    path('Scholarship/',appviews.Scholarship,name='Scholarship'),
    path('AdminHome/', views.AdminHome, name='AdminHome'),
     path('InvestorHome/', views.InvestorHome, name='InvestorHome'),



]