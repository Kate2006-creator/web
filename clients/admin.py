from django.contrib import admin

from clients.models import Client, Project, Favour, Employee, ProjectService, Review
@admin.register(Client)
class ClientAdmin (admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Project)
class ProjectAdmin (admin.ModelAdmin):
    list_display = ['name', 'client__name','deadline']

@admin.register(Favour)
class FavourAdmin (admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

@admin.register(Employee)
class EmployeeAdmin (admin.ModelAdmin):
    list_display = ['name', 'position']

@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ['project', 'favour', 'employee', 'status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['project', 'client_name', 'rating', 'created_at']

    def client_name(self, obj):
        return obj.client_name
    client_name.short_description = "Клиент"
    
    def client_email(self, obj):
        return obj.client_email
    client_email.short_description = "Email клиента"
    