from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from clients.models import Client, Project, Favour, Employee, ProjectService, Review

# Расширяем стандартную админку User
class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Профиль клиента'
    fk_name = 'user'

class EmployeeInline(admin.StackedInline):
    model = Employee  
    can_delete = False
    verbose_name_plural = 'Профиль сотрудника'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    def get_inline_instances(self, request, obj=None):
        if obj:
            # Показываем соответствующий inline в зависимости от типа профиля
            if hasattr(obj, 'client_profile'):
                return [ClientInline(self.model, self.admin_site)]
            elif hasattr(obj, 'employee_profile'):
                return [EmployeeInline(self.model, self.admin_site)]
        return []

# Перерегистрируем User админку
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'sphere', 'company_name']
    search_fields = ['user__username', 'user__userprofile__fio', 'company_name', 'sphere']
    
    def user_info(self, obj):
        return obj.user.userprofile.fio or obj.user.username
    user_info.short_description = "Клиент"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_info', 'deadline', 'status', 'budget']
    list_filter = ['status', 'start_date']
    search_fields = ['name', 'client_user__userprofile__fio', 'client_user__username']
    
    def client_info(self, obj):
        return obj.client_user.userprofile.fio or obj.client_user.username
    client_info.short_description = "Клиент"

@admin.register(Favour)
class FavourAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    search_fields = ['name', 'category']
    list_filter = ['category']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'position', 'start_work_date']
    search_fields = ['user__username', 'user__userprofile__fio', 'position']
    
    def user_info(self, obj):
        return obj.user.userprofile.fio or obj.user.username
    user_info.short_description = "Сотрудник"

@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ['project', 'favour', 'employee_info', 'status', 'hours_spent']
    list_filter = ['status', 'start_date']
    search_fields = ['project__name', 'favour__name', 'employee_user__userprofile__fio']
    
    def employee_info(self, obj):
        if obj.employee_user:
            return obj.employee_user.userprofile.fio or obj.employee_user.username
        return "Не назначен"
    employee_info.short_description = "Сотрудник"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['project', 'client_info', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['project__name', 'feedback']
    
    def client_info(self, obj):
        return obj.project.client_user.userprofile.fio or obj.project.client_user.username
    client_info.short_description = "Клиент"