from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from english.accounts.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from english.plans.models import SignaturePayment

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "accepted_the_terms_of_use")
        

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("chats:chat")
    
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    queryset = User.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        queryset = queryset.filter(pk=self.request.user.pk)
        
        return queryset
    
class SignatureRenovationsListView(LoginRequiredMixin, ListView):
    template_name = 'renovations.html'
    queryset = SignaturePayment.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(signature__user=self.request.user)
        
        return queryset