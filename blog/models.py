from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #key that conect user and task that he created (import: from django.contrib.auth.models import User)
    def __str__(self):            #func to see tittle name inthe tasks list
        return self.title    


