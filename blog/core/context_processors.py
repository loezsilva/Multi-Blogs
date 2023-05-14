from django.conf import settings

def global_configurations(request):
    return {
        "DEBUG": settings.DEBUG,
        "BASE_URL": settings.BASE_URL, 
    }