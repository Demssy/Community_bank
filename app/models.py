from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

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
