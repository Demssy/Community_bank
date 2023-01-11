from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/', null=True, blank=False)
    url = models.URLField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #key that connect user and project that he created (import: from django.contrib.auth.models import User)
    comments = GenericRelation(Comment)
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Project, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    def __str__(self):            #func to see tittle name in the tasks list
        return self.title 
    def get_absolute_url(self):
        return reverse('detailp', kwargs={'slug': self.slug})