from django.contrib.sessions.models import Session
from english.accounts.models import ActiveSession
from django.utils import timezone

def active_sessions(request):
    user = request.user
    active_session = None
    if user.is_authenticated:
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        active_session, created = ActiveSession.objects.get_or_create(
            user=user, 
            session=session,
            defaults={
                "last_activity": timezone.now()
            }
        )
        active_session.last_activity = timezone.now()
        active_session.save()
        
    return {
        "active_session": active_session
    }
    