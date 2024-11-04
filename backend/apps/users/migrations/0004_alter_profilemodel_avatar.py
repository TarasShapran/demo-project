# Generated by Django 4.2.6 on 2023-10-19 18:25

import core.services.photo_service

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profilemodel_avatar_alter_profilemodel_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=core.services.photo_service.PhotoService.upload_avatar),
        ),
    ]