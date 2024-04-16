# Generated by Django 5.0.1 on 2024-04-16 07:00

import django.core.validators
import posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missingperson',
            name='photo',
            field=models.ImageField(upload_to=posts.models.upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]
