from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from blog.accounts.models import User
from blog.posts.models import Post
from blog.pages.models import Page
# from django.views.generic import DetailView
# Create your views here.


class BlogDetailView(DetailView):
    queryset = User.objects.all()
    template_name = 'pages/blog_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        autor = self.get_object()
        object = {
            "autor": autor,
        }
        if autor.get_configuration and autor.get_configuration.header_image:
            object['header_image'] = autor.get_configuration.header_image.url
        
        context['object'] = object
        context['posts'] = Post.objects.filter(published=True)
        
        return context

class PageDetailView(DetailView):
    queryset = Page.objects.all()
    template_name = 'pages/page.html'
    
    def dispatch(self, request, *args, **kwargs):
        page = self.get_object()
        if not page.autor.get_configuration.theme.can_create_page:
            return redirect(reverse('pages:blog-detail', kwargs={ "slug": page.autor.slug }))
        
        return super().dispatch(request, *args, **kwargs)