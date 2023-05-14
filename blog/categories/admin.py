from django.contrib import admin
from .models import Category, Tag
# Register your models here.
admin.site.register([Category, Tag])