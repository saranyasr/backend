# Generated by Django 5.0.2 on 2024-09-14 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]