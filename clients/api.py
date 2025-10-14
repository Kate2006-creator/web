from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from clients.models import Client, Project, Favour, Employee, ProjectService, Review
from clients.serializers import ClientSerializer, ProjectSerializer, FavourSerializer, EmployeeSerializer, ProjectServiceSerializer, ReviewSerializer


class ClientsViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectsViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class FavoursViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Favour.objects.all()
    serializer_class = FavourSerializer

class EmployeesViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ProjectServiceViewSet(viewsets.ModelViewSet):
    queryset = ProjectService.objects.all()
    serializer_class = ProjectServiceSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

