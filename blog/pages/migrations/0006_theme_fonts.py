# Generated by Django 4.2.1 on 2023-05-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_theme_content_path_alter_theme_footer_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='fonts',
            field=models.TextField(blank=True, default='', verbose_name='Fontes do google'),
        ),
    ]
