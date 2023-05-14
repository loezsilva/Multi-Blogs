from django.db import models
from blog.core.models import BaseModel
# Create your models here.

class Comment(BaseModel):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("self", verbose_name=("Comentário"), on_delete=models.CASCADE, blank=True, null=True)
    autor = models.ForeignKey("accounts.User", verbose_name=("Autor do comentário"), related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    def childrens(self):
        return Comment.objects.filter(parent=self, approved=True) 