from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime
from english.accounts.models import ActiveSession 
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Retorna a questidade de sessões ativas em determinado momento'

    def add_arguments(self, parser):
        parser.add_argument('--minutes', default=5)
        
    def handle(self, *args, **kwargs):
        
        sessions = ActiveSession.get_active_users(minutes=int(kwargs['minutes']))
        
        print(f"Sessões ativas nos ultimos {kwargs['minutes']} minutos: {sessions.count()}")