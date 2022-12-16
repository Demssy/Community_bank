from django.urls import path
from django.contrib import admin

from scholarship import views

urlpatterns = [
    # app scholarship
    path('', views.scholarship, name = 'scholarship')

]