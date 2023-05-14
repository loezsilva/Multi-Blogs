from typing import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import pagination
from django.contrib.auth.mixins import PermissionRequiredMixin

class CheckHasPermission(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, "Você não tem permissão para acessar essa página.")
            return redirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
class SimpleAPIPagination(pagination.PageNumberPagination):       
    page_size = 20
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_size', self.get_page_size(self.request)),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
