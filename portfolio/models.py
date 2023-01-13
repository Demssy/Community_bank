from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse
class Project(models.Model):
    PROJECT_TYPE_CHOICES = (
    ('WEB_DEV', 'Web Development'),
    ('APP_DEV', 'Mobile App Development'),
    ('AI_ML', 'AI/ML Development'),
    ('DATA_ANALYSIS', 'Data Analysis'),
    ('SOFTWARE_ENG', 'Software Engineering'),
    ('GAME_DEV', 'Game Development'),
    ('ECOM_DEV', 'E-commerce Development'),
    ('IOT_DEV', 'IoT Development'),
    ('VR_AR', 'VR/AR Development'),
    ('BLOCKCHAIN', 'Blockchain Development'),
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio/images/', null=True, blank=False)
    url = models.URLField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1) #key that connect user and project that he created (import: from django.contrib.auth.models import User)
    project_type = models.CharField(max_length = 15, choices=PROJECT_TYPE_CHOICES, default = '*')
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
    def get_project_type_name(self, type):
        for choice in self.PROJECT_TYPE_CHOICES:
            if choice[0] == type:
                return choice[1]
        return ''        



class ProjectType(models.Model):
    WEB_DEV = 'WEB_DEV'
    APP_DEV = 'APP_DEV'
    AI_ML = 'AI_ML'
    DATA_ANALYSIS = 'DATA_ANALYSIS'
    SOFTWARE_ENG = 'SOFTWARE_ENG'
    GAME_DEV = 'GAME_DEV'
    ECOM_DEV = 'ECOM_DEV'
    IOT_DEV = 'IOT_DEV'
    VR_AR = 'VR_AR'
    BLOCKCHAIN = 'BLOCKCHAIN'

    PROJECT_TYPE_CHOICES = [
        (WEB_DEV, 'Web Development'),
        (APP_DEV, 'Mobile App Development'),
        (AI_ML, 'AI/ML Development'),
        (DATA_ANALYSIS, 'Data Analysis'),
        (SOFTWARE_ENG, 'Software Engineering'),
        (GAME_DEV, 'Game Development'),
        (ECOM_DEV, 'E-commerce Development'),
        (IOT_DEV, 'IoT Development'),
        (VR_AR, 'VR/AR Development'),
        (BLOCKCHAIN, 'Blockchain Development'),
    ]
    name = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)        

    def __str__(self):            #func to see tittle name in the tasks list
        return self.name