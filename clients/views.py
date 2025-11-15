#from django.http import HttpResponse
#from django.shortcuts import render

#from django.views import View
#from clients.models import Client, Project

#from django.views.generic import TemplateView

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from general.models import UserProfile

@api_view(['GET'])
def user_list(request):
    users = User.objects.prefetch_related('userprofile').all()
    data = []
    for user in users:
        data.append({
            'id': user.id, 
            'username': user.username, 
            'email': user.email,
            'userprofile': {
                'fio': user.userprofile.fio if hasattr(user, 'userprofile') else None
            } if hasattr(user, 'userprofile') else None
        })
    return Response(data)

@api_view(['GET'])
def user_list(request):
    users = User.objects.prefetch_related('userprofile').all()
    data = []
    for user in users:
        data.append({
            'id': user.id, 
            'username': user.username, 
            'email': user.email,
            'userprofile': {
                'fio': user.userprofile.fio
            } if hasattr(user, 'userprofile') and user.userprofile else None
        })
    return Response(data)

