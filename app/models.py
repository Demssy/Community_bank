from django.db import models


class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    def __str__(self):            #func to see email inthe tasks list
        return self.email

class ContactAdmin(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    def __str__(self):            #func to see email inthe tasks list
        return self.subject        





class SmmaryDataBank(models.Model):
    name=models.CharField(verbose_name='Subject name',max_length=10)
    file=models.FileField(verbose_name='summary files',upload_to='file/')
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

