from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# class Todo(models.Model):
#     title = models.CharField(max_length=100)  #title of todo
#     memo = models.TextField(blank=True)       #description by choice
#     created = models.DateTimeField(auto_now_add=True)  #time of creation todo (can't fix)
#     datecompleted = models.DateTimeField(null=True, blank=True)    #date and time where task was comleted 
#     important = models.BooleanField(default=False)     #if task is important
#     user = models.ForeignKey(User, on_delete=models.CASCADE) #key that conect user and task that he created (import: from django.contrib.auth.models import User)

#     def __str__(self):            #func to see tittle name inthe tasks list
#         return self.title

class User(AbstractBaseUser):
    STUDENT = 1
    INVESTOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (INVESTOR, 'Investor'),
        (ADMIN, 'Admin')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False)