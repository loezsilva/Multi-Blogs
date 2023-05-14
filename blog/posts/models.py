from django.db import models
from tinymce.models import HTMLField
from blog.core.models import BaseModel
from django_lifecycle import hook
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.urls import reverse

# Create your models here.

def post_upload_to(instance, filename):
    return f"post/covers/{instance}-{filename}"

class Post(BaseModel):
    title = models.CharField(max_length=200)
    image = models.ImageField("Capa do post", upload_to=post_upload_to, max_length=5000)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    autor = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = HTMLField()
    published = models.BooleanField(default=False)
    categories = models.ManyToManyField('categories.Category')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        
    @hook('before_create')
    def create_slug(self):
        self.slug = slugify(self.title)
        
    def get_absolute_url(self):
        return reverse("pages:post-detail", kwargs={"slug": self.slug})
    
    @property
    def urls(self):
        return {
            "change": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.pk,)),
            "delete": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_delete', args=(self.pk,))
        }
    
    @property
    def content_str(self):
        return strip_tags(self.content)