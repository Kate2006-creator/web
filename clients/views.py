from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from clients.models import Client, Project

from django.views.generic import TemplateView

# Create your views here.

class ShowClientsView(View):
    def get(request, *args, **kwargs):
        clients = Client.objects.all()

        result = ""
        for s in clients:
            result += s.name + "<br>"

        return HttpResponse(result)

class ClientsListTemplate(TemplateView):
    template_name = "clients/list.html"

    def get_context_data(self, **kwargs):

        clients = Client.objects.all()

        return {'items': clients}
    
class ProjectsListTemplate(TemplateView):
    template_name = "clients/list.html"

    def get_context_data(self, **kwargs):

        projects = Project.objects.all()

        return {'items': projects}