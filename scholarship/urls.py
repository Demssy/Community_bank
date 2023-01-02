from django.urls import path
from django.contrib import admin
from scholarship import views

urlpatterns = [
    # app scholarship
    path('scolarships/', views.scholarship, name = 'scholarship'),
    path('scolarships/create/', views.create_scolarship, name = 'create_scolarship'),
    path('scholarships/<int:scholarship_id>/delete/', views.delete_scholarship, name='delete_scholarship'),
    path('scholarships/all/', views.all_scholarship, name='all_scholarship'),

]