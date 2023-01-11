from django.urls import reverse
import datetime
import os
from django.conf import settings
from django.db import models
from app import models as m1
from app.models import Scholarship
 
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_avatar = models.ImageField(upload_to='user_profile/avatars/',default='user_profile/avatars/default.jpg')
    is_student = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    mailing_address = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, null=True ,blank=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    bio = models.TextField(max_length=350, null=True ,blank=True)
    Scholarship = models.ManyToManyField(Scholarship,blank=True)
  




    def create_user(username, email, password, first_name, last_name, college=None, major=None, gender=None, date_of_birth=None, bio=None, user_avatar=None):
        user = CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            college=college,
            major=major,
            gender=gender,
            date_of_birth=date_of_birth,
            bio=bio,
            user_avatar=user_avatar)
        user.set_password(password)
        user.save()
        return user

        

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.user_avatar.storage, self.user_avatar.path
        # Delete the model before the file
        super(CustomUser, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    def __str__(self):            #func to see tittle name in the tasks list
        return self.username

    def save(self, *args, **kwargs):
        # Override the save method to automatically set the `is_student` field to True if the `college` field is filled in
        if self.college:
            self.is_student = True
            super(CustomUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # Return the URL for the user's profile page
        return reverse('user_profile', args=[self.pk])

    def total_scholarship_amount(self):
        total = 0
        for scholarship in self.Scholarship.all():
            total += scholarship.Amount
        return total

