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
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('contactus/', views.contactus, name='contactus'),
    path('contactadmin/', views.contactadmin, name='contactadmin'),
    path('personalArea/', views.personalArea, name='personalArea'),
    path('userSettings/', views.userSettings, name = 'userSettings'),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls'), name = 'blog'),
    path('comment/', include('comment.urls', namespace = 'comment')),
    path('api/', include('comment.api.urls')),
    path('search', views.search, name = 'search'),
    path('messages/', include('postman.urls', namespace='postman')),
    path('user_profile/', include('accounts.urls'), name= 'accounts'),
    path('SmmaryDataBank/', views.SmmaryDataBank, name='SmmaryDataBank'),
    path('donations/', views.donations, name='donations'),
    path('Scholarship/', views.Scholarship, name='Scholarship'),
    path('addscholarship/<int:id>/', views.add_ScholarShip, name='addscholarship'),
    path('reports/', views.reports, name='reports'),
    path('cancelScholarship/', views.cancelScholarship, name='cancelScholarship'),
    path('setingUsers/', views.setingUsers, name='setingUsers'),
    path('getScolarship/', views.getScolarship, name='getScolarship'),
    path('AddScholarshipINVESOR/', views.AddScholarshipINVESOR, name='AddScholarshipINVESOR'),
    path('selectOption/', views.selectOption, name='selectOption'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
