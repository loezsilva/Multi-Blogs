# Generated by Django 4.2.1 on 2023-05-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='has_navbar',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='theme',
            name='has_sidebar',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
