from rest_framework import serializers
from clients.models import Client, Project, Favour, Employee, ProjectService, Review


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
    
class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'client_user', 'deadline', 'budget', 'status', 'description']

class FavourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favour
        fields = ['id', 'name', 'category', 'description', 'price']
    

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'position', 'start_work_date'] 

class ProjectServiceSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    favour = FavourSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = ProjectService
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(read_only=True)
    client_email = serializers.CharField(read_only=True)
    project_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'project', 'project_name', 'client_name', 'client_email', 
                 'rating', 'feedback', 'created_at']

