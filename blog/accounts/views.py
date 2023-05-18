from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView
from .models import User, BlogConfiguration
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.pages.models import Theme
from django.conf import settings

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("avatar", "username", "name", "blog_name",  "accepted_the_terms_of_use")

class BlogConfigurationUpdateForm(forms.ModelForm):
    
    class Meta:
        model = BlogConfiguration
        exclude = ("autor", )
    
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
    template_name = 'accounts/blog_configuration_update.html'
    form_class = BlogConfigurationUpdateForm
    queryset = BlogConfiguration.objects.all()
    
    def get_success_url(self):
        blog = self.get_object().autor
        return blog.get_absolute_url()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(autor=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["themes"] = Theme.objects.all()
        return context
    