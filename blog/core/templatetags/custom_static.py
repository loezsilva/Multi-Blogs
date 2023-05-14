from django import template
from django.templatetags.static import static
from django.template.defaultfilters import safe

register = template.Library()

@register.simple_tag
def static_safed(path):
    return safe(f"{static(path)}")

@register.simple_tag
def custom_static(configuration, path):
    if theme := configuration.theme:
        return f"{static(theme.path +'/'+ path)}"
    
    return static(path)