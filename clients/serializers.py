from rest_framework import serializers
from clients.models import Client, Project, Favour, Employee, ProjectService, Review
from django.contrib.auth.models import User
from general.models import UserProfile


# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_profile = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Client
        fields = "__all__"
    
    def get_user_profile(self, obj):
        if hasattr(obj.user, 'userprofile'):
            return {
                'fio': obj.user.userprofile.fio
            }
        return None
    
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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio', 'birthday']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'userprofile']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user