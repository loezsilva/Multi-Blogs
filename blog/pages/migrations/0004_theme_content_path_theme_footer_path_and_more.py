# Generated by Django 4.2.1 on 2023-05-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_theme_has_header_alter_theme_has_navbar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='content_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Pasta do tema'),
        ),
        migrations.AddField(
            model_name='theme',
            name='footer_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Pasta do tema'),
        ),
        migrations.AddField(
            model_name='theme',
            name='navbar_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Pasta do tema'),
        ),
        migrations.AddField(
            model_name='theme',
            name='sidebar_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Pasta do tema'),
        ),
    ]
