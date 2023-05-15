from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from blog.accounts.models import User, ActiveSession, SocialAccount, BlogConfiguration

admin.site.register([SocialAccount, BlogConfiguration])

@admin.register(ActiveSession)
class ActiveSessionAdmin(admin.ModelAdmin):
    '''Admin View for ActiveSession'''

    list_display = ('user', 'last_activity')
    list_filter = ('user', 'last_activity')
    date_hierarchy = 'last_activity'
    ordering = ('last_activity',)

@admin.register(User)
class ActiveSessionAdmin(admin.ModelAdmin):
    '''Admin View for ActiveSession'''
    list_display = ('email', 'blog')
    search_fields = ('email', )
    ordering = ('-date_joined', )
    
    def blog(self, obj):
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=reverse('pages:blog-detail', kwargs={ "slug": obj.slug }))