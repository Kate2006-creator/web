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
        fields = ['id', 'user', 'position', 'start_work_date', 'picture'] 

# class ProjectServiceSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(read_only=True)
#     favour = FavourSerializer(read_only=True)
#     employee = EmployeeSerializer(read_only=True)
    
#     class Meta:
#         model = ProjectService
#         fields = '__all__'

class ProjectServiceSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    favour_name = serializers.CharField(source='favour.name', read_only=True)
    employee_username = serializers.CharField(source='employee_user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = ProjectService
        fields = [
            'id', 'project', 'favour', 'employee_user', 'status', 
            'start_date', 'end_date', 'hours_spent', 'notes',
            'project_name', 'favour_name', 'employee_username'
        ]
        read_only_fields = ('start_date', 'id')


class ReviewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(read_only=True)
    client_email = serializers.CharField(read_only=True)
    project_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'project', 'project_name', 'client_name', 'client_email', 
                 'rating', 'feedback', 'created_at', 'picture']

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