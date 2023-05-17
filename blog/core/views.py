from django.shortcuts import render
from django.views.generic import ListView
from blog.accounts.models import User
from django.db.models import Count

# Create your views here.
class IndexListView(ListView):
    queryset = User.objects.all()
    template_name = 'core/index.html'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total_posts=Count('post')).order_by('-total_posts')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_blog = self.get_queryset().first()
        context["main_blog"] = main_blog
        context["object_list"] = self.get_queryset().exclude()
        return context
    