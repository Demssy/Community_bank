from django.contrib import admin
from .models import ContactUsModel, ContactAdmin

admin.site.register(ContactUsModel)
admin.site.register(ContactAdmin)
