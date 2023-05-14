from django.contrib import admin
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
    list_display = ('email', )
    search_fields = ('email', )
    ordering = ('-date_joined', )