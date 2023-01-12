from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #key that conect user and task that he created (import: from django.contrib.auth.models import User)
    comments = GenericRelation(Comment)
    def __str__(self):            #func to see tittle name inthe tasks list
        return self.title    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})


