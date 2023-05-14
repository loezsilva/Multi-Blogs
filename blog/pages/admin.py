from django.contrib import admin
from .models import Page, Theme
# Register your models here.
admin.site.register([Page, Theme])