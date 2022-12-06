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
from portfolio.views import userPortfolio

urlpatterns = [
    path('admin/', admin.site.urls),                              #admin path
    #Auth
    path('signup/', views.signupuser, name='signupuser'),         #auth path
    path('login/', views.loginuser, name='loginuser'),            #login path
    path('logout/', views.logoutuser, name='logoutuser'),         #logout path
    #Home
    path('', views.home, name='home'),                            #home page path 
    #Personal area
    path('PersonalArea/', views.PersonalArea, name='PersonalArea'),
    #app portfolio
    path('Portfolio/', include('portfolio.urls')),
    #app blog
    path('blog/', include('blog.urls')),
    # path('create/', views.createtodo, name='createtodo'),         #create todo
    # path('current/', views.currenttodos, name='currenttodos'),    #current path
    # path('completed/', views.completedtodos, name='completedtodos'),
    # path('<int:todo_pk>', views.viewtodo, name='viewtodo'),  #todo view(open page vith specific todo)
    # path('<int:todo_pk>/complete', views.completetodo, name='completetodo'), #complete todo
    # path('<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),  #delete todo
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)