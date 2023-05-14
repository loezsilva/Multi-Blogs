from django.contrib import admin
from blog.comments.models import Comment

# Register your models here.
admin.site.register([Comment])