from django.urls import path
from django.contrib import admin
from django.conf.urls import url

urlpatterns = [
    # app scholarship
    path('scholarship/', include('scholarship.urls')),

]