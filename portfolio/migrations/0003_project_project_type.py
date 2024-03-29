# Generated by Django 4.1.5 on 2023-01-12 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('WEB_DEV', 'Web Development'), ('APP_DEV', 'Mobile App Development'), ('AI_ML', 'AI/ML Development'), ('DATA_ANALYSIS', 'Data Analysis'), ('SOFTWARE_ENG', 'Software Engineering'), ('GAME_DEV', 'Game Development'), ('ECOM_DEV', 'E-commerce Development'), ('IOT_DEV', 'IoT Development'), ('VR_AR', 'VR/AR Development'), ('BLOCKCHAIN', 'Blockchain Development')], default='*', max_length=20),
        ),
    ]
