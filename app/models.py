from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class ContactUsModel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class ContactAdmin(models.Model):
    subject = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
        #


# from app.models import Scholarship
# from accounts.models import CustomUser
class Scholarship(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    Location = models.CharField(max_length=100)
    requirements = models.CharField(max_length=500)
    Amount = models.CharField(max_length=50)
    Hours = models.CharField(max_length=50)




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

class DonationsModel(models.Model):
    CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'
    VERIFICATION_VALUE_RE = r'^([0-9]{3,4})$'
    EXPIRY_DATE_VALUE_RE = r'^\d{2}-\d{2}$'
    amount = models.DecimalField(max_digits=4, decimal_places=0)
    scholarship = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    nameOnCard = models.CharField(max_length=50, blank=False, default='')
    cardNumber = models.CharField(
    max_length=30,
    default=0,
    blank=False,
    validators=[RegexValidator(regex=CREDIT_CARD_RE,message='Please enter a valid credit card number.',code='invalid_credit_card')])
    expiryDate = models.CharField(
    max_length=5,
    default='MM-YY',
    blank=False,
    validators=[
        RegexValidator(
            regex=EXPIRY_DATE_VALUE_RE,
            message='Please enter a valid expiry date.',
            code='invalid_expiry_date'
        ),
    ])
    cardCode = models.CharField(
    max_length=4,
    blank=False,
    default=0,
    validators=[
        RegexValidator(
            regex=VERIFICATION_VALUE_RE,
            message='Please enter a valid verification code (3/4 digits).',
            code='invalid_verification_code'
        ),
    ])
    def __str__(self):
        return self.reason





