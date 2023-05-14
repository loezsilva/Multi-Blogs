from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from blog.posts.models import Post
from blog.comments.models import Comment
from django.contrib import messages

# Create your views here.

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'pages/post.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.GET:
            data = request.GET
            comment, created = Comment.objects.get_or_create(
                post=self.get_object(),
                autor=self.request.user,
                parent=Comment.objects.get(pk=data.get('parent')) if data.get('parent') else None,
                text=data.get('text')
            )
            
            if created:
                messages.success(request, "Comentário adicionado com sucesso, agora é só aguardar a aprovação.")
            else:
                messages.warning(request, "O comentário já enviado.")
                
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.get_object(), approved=True)
        return context
    