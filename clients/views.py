from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from clients.models import Client

# Create your views here.

class ShowClientsView(View):
    def get(request, *args, **kwargs):
        clients = Client.objects.all()

        result = ""
        for s in clients:
            result += s.name + "<br>"

        return HttpResponse(result)
