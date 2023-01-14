from django.contrib import admin
from .models import Blog


class BlogectAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    ordering = ['id']



admin.site.register(Blog)

