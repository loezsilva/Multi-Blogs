import os
import tinymce.models
import uuid
import urllib.request
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from django.core import management
from blog.pages.models import Theme
from tinymce.models import HTMLField
from blog.core.models import BaseModel
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import gettext_lazy as _
from django_lifecycle import hook, LifecycleModelMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.template.defaultfilters import slugify



def avatar_upload_to(instance, filename):
    return f"avatar/{instance}-{filename}"

def header_upload_to(instance, filename):
    return f"headers/{instance}-{filename}"

class User(LifecycleModelMixin, PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    
    avatar = models.ImageField("Imagem", upload_to=avatar_upload_to, blank=True, null=True, max_length=5000)
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=('150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    
    name = models.CharField('Seu nome', max_length=200, default="Usuário sem nome")
    
    blog_name = models.CharField('Nome do seu blog', max_length=200, blank=True)
    
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    
    email = models.EmailField(_('email address'), unique=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    CLIENT, OWNER = range(2)
    
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    accepted_the_terms_of_use = models.BooleanField("Aceitou os termos de uso da plataforma", default=False, blank=True)
    
    about_me = models.TextField("Sobre mim", blank=True, null=True)
    
    profile_views = models.IntegerField("Visitas do perfil", default=0, blank=True)
        
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("pages:blog-detail", kwargs={"slug": self.slug})
    
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def urls(self):
        return  {}

    @hook('after_create')
    def create_token(self):
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=self)
        
    @hook('after_create')
    def create_blog_configuration(self):
        if not Theme.objects.exists():
            management.call_command('import_themes')
            
        BlogConfiguration.objects.get_or_create(
            autor=self,
            name=self.blog_name,
            theme=Theme.objects.all().order_by('created_at').first()
        )
        
    @hook('before_create')
    def create_slug_and_set_email(self):
        if self.blog_name:
            self.slug = slugify(self.blog_name)
        else:
            self.slug = slugify(get_random_string(50))
        
        if not self.email:
            self.email = self.username
    
    @hook('before_create')
    def check_permission(self):
        if not settings.MULTIBLOGS and User.objects.all().count() > 0:
            raise PermissionError("Não é possível adicionar novos blogs com a configuração de MULTIBLOGS=False, altere o seu .env para MULTIBLOGS=True")
        
    @hook('after_create')
    def set_superuser(self):
        if not User.objects.filter(is_superuser=True).exists():
            if user := User.objects.all().order_by('-date_joined').first():
                user.is_superuser = True
                user.is_staff = True
                user.save(skip_hooks=True)
    
    def save_image_from_url(self, url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib.request.urlopen(url).read())
        img_temp.flush()
        filename = os.path.basename(url)
        
        self.avatar.save(filename, File(img_temp), save=True)
        
    @property
    def get_avatar_url(self):        
        if not self.avatar:
            self.save_image_from_url(f"https://avatars.dicebear.com/v2/avataaars/{get_random_string(50)}.svg")
            
        return self.avatar.url
    
    @property
    def get_configuration(self):
        if hasattr(self, 'configuration'):
            return self.configuration
        return None
    
    def pages(self):
        from blog.pages.models import Page
        return Page.objects.filter(autor=self, published=True)

class SocialAccount(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SOCIAL_CHOICES = (
        ('facebook', "Facebook"),
        ('twitter', "Twitter"),
        ('instagram', "Instagram"),
        ('twitch', "Twitch"),
        ('youtube', "Youtube"),
        ('patreon', "Patreon"),
        ('discord', "Discord"),
    )
    social = models.CharField("Rede social", max_length=50, choices=SOCIAL_CHOICES)
    url = models.URLField("Link do perfil", max_length=255)
    icon = models.CharField("Ícone da rede social", max_length=50, blank=True)
    
    def get_icon(self):    
        if self.icon:
            return self.icon
        
        icons = {
            "facebook": "fa-brands fa-facebook",
            "twitter": "fa-brands fa-twitter",
            "instagram": "fa-brands fa-instagram",
            "twitch": "fa-brands fa-twitch",
            "youtube": "fa-brands fa-youtube",
            "patreon": "fa-brands fa-patreon",
            "discord": "fa-brands fa-discord",
        }
        
        return icons[self.social]

class ActiveSession(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()

    @classmethod
    def get_active_users(cls, minutes=5):
        """
        Retorna uma lista de usuários que tiveram atividade nos últimos `minutes` minutos.
        """
        active_sessions = cls.objects.filter(last_activity__gte=timezone.now() - timezone.timedelta(minutes=minutes))
        
        active_users = User.objects.filter(pk__in=active_sessions.values('user'))
        
        return active_users
    
    def __str__(self):
        return f'{self.user}, ultima sessão: {self.last_activity}'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Sessão ativa'
        verbose_name_plural = 'Sessões ativas'
        
class BlogConfiguration(BaseModel):
    autor = models.OneToOneField(User, verbose_name=_("Autor do blog"), related_name="configuration", on_delete=models.CASCADE)
    header_image = models.ImageField("Capa do blog", upload_to=header_upload_to, blank=True, null=True, max_length=5000)
    name = models.CharField("Nome do blog", max_length=200)
    description = HTMLField()
    theme = models.ForeignKey("pages.Theme", verbose_name=_("Tema do blog"), on_delete=models.CASCADE, blank=True, null=True)
    
    show_post_image = models.BooleanField("Mostrar imagem do post", default=True, blank=True)
    show_post_header = models.BooleanField("Mostrar header do post", default=True, blank=True)
    show_comments = models.BooleanField("Mostrar comentários", default=True, blank=True)
    auto_approve_comments = models.BooleanField("Aprovar comentários automaticamente", default=False, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        
    @property
    def urls(self):
        return {
            "add": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_add'),
            "change": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.pk,)),
            "delete": reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_delete', args=(self.pk,))
        }
    
    @property
    def description_str(self):
        return strip_tags(self.description)