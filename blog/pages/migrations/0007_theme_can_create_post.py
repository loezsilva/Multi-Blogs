# Generated by Django 4.2.1 on 2023-05-15 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_theme_fonts'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='can_create_post',
            field=models.BooleanField(blank=True, default=True, verbose_name='O tema pode criar posts'),
        ),
    ]
