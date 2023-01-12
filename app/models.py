from django.db import models
from django.contrib.auth.models import AbstractUser


class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):  # func to see email inthe tasks list
        return self.email


class ContactAdmin(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):  # func to see email inthe tasks list
        return self.subject
    #


class Scholarship(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    Location = models.CharField(max_length=100)
    requirements = models.CharField(max_length=250)
    Amount = models.CharField(max_length=50)
    Hours = models.CharField(max_length=50)
    image = models.ImageField(upload_to="scholarship/images")

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Scholarship, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


    def __str__(self):
        return self.title


class SmmaryDataBank(models.Model):
    name = models.CharField(verbose_name='Subject name', max_length=10)
    file = models.FileField(verbose_name='summary files', upload_to='file/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SmmaryDataBank(models.Model):
    name = models.CharField(verbose_name='Subject name', max_length=10)
    file = models.FileField(verbose_name='summary files', upload_to='file/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DonationsModel(models.Model):
    amount = models.DecimalField(max_digits=4, decimal_places=0)
    scholarship = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.reason
