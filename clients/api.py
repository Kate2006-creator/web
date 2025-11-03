from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from clients.models import Client, Project, Favour, Employee, ProjectService, Review
from clients.serializers import ClientSerializer, ProjectSerializer, FavourSerializer, EmployeeSerializer, ProjectServiceSerializer, ReviewSerializer


class ClientsViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectsViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class FavoursViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = Favour.objects.all()
    serializer_class = FavourSerializer

class EmployeesViewset(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ProjectServiceViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = ProjectService.objects.all()
    serializer_class = ProjectServiceSerializer

class ReviewViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

