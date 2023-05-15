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
            "fonts": """
                <!-- Google fonts-->
                <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
                <link href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800" rel="stylesheet" type="text/css" />
            """,
            "has_navbar": True,
            "has_sidebar": False,
            "has_header": True,
        },
        {
            "name": "Resume",
            "description": "",
            "path": "resume",
            "fonts": """
                <!-- Google fonts-->
                <link href="https://fonts.googleapis.com/css?family=Saira+Extra+Condensed:500,700" rel="stylesheet" type="text/css" />
                <link href="https://fonts.googleapis.com/css?family=Muli:400,400i,800,800i" rel="stylesheet" type="text/css" />
            """,
            "has_navbar": False,
            "has_sidebar": True,
            "has_header": False,
        }
    ]

    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **kwargs):
        for theme in self.themes:
            Theme.objects.update_or_create(
                name=theme.get('name'),
                defaults=theme
            )