from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from blog.core.models import BaseModel
from django_lifecycle import hook
from django.template.defaultfilters import slugify

# Create your models here.
class Page(BaseModel):
    autor = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField("Nome do link da página", max_length=50, default="Página", blank=True)
    title = models.CharField("Título da página", max_length=200)
    subtitle = models.CharField("Subtítulo da página", max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = HTMLField()
    published = models.BooleanField(default=False)
    order = models.SmallIntegerField("Ordem da página", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-order']
        
    @hook('before_create')
    def create_page_name(self):
        return f"Página {Page.objects.filter(autor=self.autor).count() + 1}"
    
    @hook('before_create')
    def create_slug(self):
        self.slug = slugify(self.title)
        
    def get_absolute_url(self):
        return reverse("pages:page-detail", kwargs={"slug": self.slug})
    
    @property
    def urls(self):
        return {
            "change": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.pk,)),
            "delete": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_delete', args=(self.pk,))
        }
    @hook('before_create')
    def create_order(self):
        self.order = Page.objects.filter(autor=self.autor).count() + 1
    
class Theme(BaseModel):
    name = models.CharField("Nome do tema", max_length=50)
    description = HTMLField()
    path = models.CharField("Pasta do tema", max_length=50)
    image_url = models.URLField("Image do Tema", max_length=255, default="")
    fonts = models.TextField("Fontes do google", default="", blank=True)
    
    navbar_path = models.CharField("Path do navbar", max_length=200, blank=True)
    sidebar_path = models.CharField("Path do sidebar", max_length=200, blank=True)
    content_path = models.CharField("Path do conteúdo", max_length=200, blank=True)
    footer_path = models.CharField("Path do footer", max_length=200, blank=True)
    
    has_navbar = models.BooleanField("O tema mostra o navbar",default=True, blank=True)
    has_sidebar = models.BooleanField("O tema mostra o sidebar", default=False, blank=True)
    has_header = models.BooleanField("O tema mostra o header", default=False, blank=True)
    
    can_create_post = models.BooleanField("O tema pode criar posts", default=True, blank=True)
    can_create_page = models.BooleanField("O tema pode criar páginas", default=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @hook('before_create')
    @hook('before_update')
    def populate_paths(self):        
        self.navbar_path = f'core/{self.path}/includes/navbar.html'
        self.sidebar_path = f'core/{self.path}/includes/sidebar.html'
        self.content_path = f'core/{self.path}/includes/content.html'
        self.footer_path = f'core/{self.path}/includes/footer.html'

    class Meta:
        ordering = ['-created_at']