# Generated by Django 4.1.5 on 2023-01-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_college_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='major',
            field=models.CharField(choices=[('CE', 'Computer Engineering'), ('ME', 'Mechanical Engineering'), ('EE', 'Electrical Engineering'), ('CEE', 'Civil and Environmental Engineering'), ('IE', 'Industrial Engineering'), ('AE', 'Aerospace Engineering'), ('PE', 'Petroleum Engineering'), ('CHE', 'Chemical Engineering'), ('BT', 'Biotechnology'), ('MSE', 'Materials Science and Engineering'), ('OE', 'Ocean Engineering'), ('NE', 'Nuclear Engineering'), ('SE', 'Software Engineering')], max_length=5),
        ),
    ]
