# Generated by Django 4.1.5 on 2023-01-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_merge_20230114_1504'),
        ('accounts', '0013_alter_customuser_major'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Scholarship',
            field=models.ManyToManyField(related_name='users', to='app.scholarship'),
        ),
    ]