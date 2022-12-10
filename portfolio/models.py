from django.db import models
from django.contrib.auth.models import User
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/')
    url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #key that conect user and task that he created (import: from django.contrib.auth.models import User)
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Project, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    def __str__(self):            #func to see tittle name inthe tasks list
        return self.title 
