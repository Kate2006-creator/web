from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from clients.models import Client, Project, Favour, Employee, ProjectService, Review
from django.contrib.auth.models import User
from general.models import UserProfile
from clients.serializers import ClientSerializer, ProjectSerializer, FavourSerializer, EmployeeSerializer, ProjectServiceSerializer, ReviewSerializer, UserSerializer, UserProfileSerializer


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

class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer