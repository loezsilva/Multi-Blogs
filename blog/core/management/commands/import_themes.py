from django.db.models import Q
from django.core.management.base import BaseCommand
from django.conf import settings
from blog.pages.models import Theme

class Command(BaseCommand):
    help = 'Cria os temas'
    themes = [
        {
            "name": "Clean blog",
            "description": "",
            "path": "clean-blog",
        }
    ]

    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **kwargs):
        for theme in self.themes:
            Theme.objects.get_or_create(**theme)