from django.urls import path
from django.contrib import admin
from . import views 

urlpatterns = [
    # app scholarship
    path('scholarships/', views.scholarship, name = 'scholarship'),
    path('scholarships/create/', views.create_schlarship, name = 'create_scholarship'),
    path('scholarships/<int:scholarship_id>/delete/', views.delete_scholarship, name='delete_scholarship'),
    path('scholarships/all/', views.all_scolarship, name='all_scholarship'),

]