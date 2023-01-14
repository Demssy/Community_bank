from django.urls import reverse
import datetime
import os
from django.conf import settings
from django.db import models
from app import models as m1
from app.models import Scholarship
 
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    )

    COLLEGE_CHOICES = (
    ('HEBR', 'Hebrew University of Jerusalem'),
    ('TAU', 'Tel Aviv University'),
    ('TECH', 'Technion - Israel Institute of Technology'),
    ('BGU', 'Ben-Gurion University of the Negev'),
    ('WEIZ', 'Weizmann Institute of Science'),
    ('BIU', 'Bar-Ilan University'),
    ('HAIFA', 'University of Haifa'),
    ('ARIEL', 'Ariel University'),
    ('OPEN', 'Open University of Israel'),
    ('ONO', 'Ono Academic College'),
    ('IDC', 'Interdisciplinary Center Herzliya'),
    ('BEZ', 'Bezalel Academy of Arts and Design'),
    ('HUJI', 'The Hebrew University of Jerusalem'),
    ('SCE', 'Shamoon College of Engineering')
    )
    MAJOR_CHOICES = (
    ('CE', 'Computer Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('EE', 'Electrical Engineering'),
    ('CEE', 'Civil and Environmental Engineering'),
    ('IE', 'Industrial Engineering'),
    ('AE', 'Aerospace Engineering'),
    ('PE', 'Petroleum Engineering'),
    ('CHE', 'Chemical Engineering'),
    ('BT', 'Biotechnology'),
    ('MSE', 'Materials Science and Engineering'),
    ('OE', 'Ocean Engineering'),
    ('NE', 'Nuclear Engineering'),
    ('SE', 'Software Engineering'),
    )
    user_avatar = models.ImageField(upload_to='user_profile/avatars/',default='user_profile/avatars/default.jpg')
    is_student = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    mailing_address = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=5, choices=COLLEGE_CHOICES)
    major = models.CharField(max_length=5, choices=MAJOR_CHOICES)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES ,null=True ,blank=True)
    date_of_birth = models.DateField()
    bio = models.TextField(max_length=350, null=True ,blank=True)
    #Scholarship = models.ManyToManyField(Scholarship,blank=True)
  




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
        else:
            self.is_investor = True
            self.is_student = False    
            super(CustomUser, self).save(*args, **kwargs)    

    def get_absolute_url(self):
        # Return the URL for the user's profile page
        return reverse('user_profile', args=[self.pk])

    def total_scholarship_amount(self):
        total = 0
        for scholarship in self.Scholarship.all():
            total += scholarship.Amount
        return total

