from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView
from .models import User, BlogConfiguration
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("avatar", "username", "first_name", "accepted_the_terms_of_use")
    
class BlogCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/blog_creation.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not settings.MULTIBLOGS and User.objects.all().count() > 0:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        blog = self.object
        return reverse('accounts:blog-configuration-update', kwargs={ "pk": blog.get_configuration.id })
    
class BlogConfigurationUpdateView(LoginRequiredMixin, UpdateView):
    fields = "__all__"
    model = BlogConfiguration
    template_name = 'accounts/blog_configuration_update.html'
    
    def get_success_url(self):
        blog = self.get_object()
        return redirect(blog.get_absolute_url())