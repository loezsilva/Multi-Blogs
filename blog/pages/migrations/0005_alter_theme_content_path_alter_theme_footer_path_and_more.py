# Generated by Django 4.2.1 on 2023-05-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_theme_content_path_theme_footer_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='content_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Path do conteúdo'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='footer_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Path do footer'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='navbar_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Path do navbar'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='sidebar_path',
            field=models.CharField(blank=True, max_length=200, verbose_name='Path do sidebar'),
        ),
    ]
