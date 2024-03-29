# Generated by Django 4.1.5 on 2023-01-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_project_project_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('WEB_DEV', 'Web Development'), ('APP_DEV', 'Mobile App Development'), ('AI_ML', 'AI/ML Development'), ('DATA_ANALYSIS', 'Data Analysis'), ('SOFTWARE_ENG', 'Software Engineering'), ('GAME_DEV', 'Game Development'), ('ECOM_DEV', 'E-commerce Development'), ('IOT_DEV', 'IoT Development'), ('VR_AR', 'VR/AR Development'), ('BLOCKCHAIN', 'Blockchain Development')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('WEB_DEV', 'Web Development'), ('APP_DEV', 'Mobile App Development'), ('AI_ML', 'AI/ML Development'), ('DATA_ANALYSIS', 'Data Analysis'), ('SOFTWARE_ENG', 'Software Engineering'), ('GAME_DEV', 'Game Development'), ('ECOM_DEV', 'E-commerce Development'), ('IOT_DEV', 'IoT Development'), ('VR_AR', 'VR/AR Development'), ('BLOCKCHAIN', 'Blockchain Development')], default='*', max_length=15),
        ),
    ]
