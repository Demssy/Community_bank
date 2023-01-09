"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views   
from django.conf.urls.static import static    
from django.conf import settings   


urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    #Home
    path('', views.home, name='home'),
    #Contactus
    path('contactus/', views.contactus, name='contactus'),
    #contactAdmin
    path('contactadmin/', views.contactadmin, name='contactadmin'),
    #Personal area
    path('personalArea/', views.personalArea, name='personalArea'),
    path('userSettings/', views.userSettings, name = 'userSettings'),
    #app portfolio
    path('portfolio/', include('portfolio.urls')),
    #app blog
    path('blog/', include('blog.urls'), name = 'blog'),
    #comments
    path('comment/', include('comment.urls', namespace = 'comment')),
    #path('api/', include('comment.api.urls')),  # only required for API Framework
    #search
    path('search', views.search, name = 'search'),
    #scholarship
    #path('scholarship/', include('scholarship.urls'), name = 'scholarships'),
    #path('SmmaryDataBank/', views.SmmaryDataBank, name='SmmaryDataBank'),
    #messages
    #path('messages/', include('postman.urls', namespace='postman')),
    #user_profile
    path('user_profile/', include('accounts.urls'), name= 'accounts'),
    path('SmmaryDataBank/', views.SmmaryDataBank, name='SmmaryDataBank'),
    path('Scholarship/', views.Scholarship, name='Scholarship'),
   # path('AdminPage/', views.AdminPage, name='AdminPage'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)