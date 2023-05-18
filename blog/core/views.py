from django.shortcuts import render, redirect
from django.views.generic import ListView
from blog.accounts.models import User
from django.db.models import Count
from django.conf import settings

# Create your views here.
class IndexListView(ListView):
    queryset = User.objects.annotate(total_posts=Count('post'))
    template_name = 'core/index.html'
    paginate_by = 6
    
    def dispatch(self, request, *args, **kwargs):
        if not settings.MULTIBLOGS:
            if blog := self.queryset.order_by('-date_joined').first():
                return redirect(blog.get_absolute_url())
            else:
                return redirect('accounts:blog-creation')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset().order_by('-total_posts')
        
        main_blog = queryset.first()
        context["main_blog"] = main_blog
        context["object_list"] = queryset.exclude()
        return context
    