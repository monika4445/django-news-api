# Generated by Django 4.2.13 on 2024-05-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
