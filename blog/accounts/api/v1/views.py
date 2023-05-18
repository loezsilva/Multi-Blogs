from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from blog.accounts.models import User

class CheckBlogAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def get(self, request, *args, **kwargs):
        
        data = request.GET
        
        if blog := User.objects.filter(slug=data.get('slug')).exists():
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND)