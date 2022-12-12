
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    def __str__(self):            #func to see email inthe tasks list
        return self.email

# class userProfile(models.Model):
#     name = models.CharField(max_length=100)
#     emai = models.EmailField()
#     institution = models.CharField(max_length=150)
#     image = models.ImageField(upload_to='app/images/')
#     aboutMe = models.CharField(max_length=300)


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
