from .models import Post
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = ('title', 'ver_no_site')
    list_filter = ('published', 'autor')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    
    def ver_no_site(self, obj):
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=reverse('pages:post-detail', kwargs={ "slug": obj.slug }))