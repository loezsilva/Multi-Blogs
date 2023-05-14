from django.db import models
from blog.core.models import BaseModel
from django_lifecycle import hook
from django.template.defaultfilters import slugify

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
        
    @hook('before_create')
    def create_slug(self):
        self.slug = slugify(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"

    @hook('before_create')
    def create_slug(self):
        self.slug = slugify(self.name)