from django.contrib import admin
from django.urls import include, path

from clients import views
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls

from django.conf import settings
from django.conf.urls.static import static

from clients.api import ClientsViewset, ProjectsViewset, FavoursViewset, EmployeesViewset, ProjectServiceViewSet, ReviewViewSet, UserViewSet,UserProfileViewSet

router = DefaultRouter()
router.register("clients", ClientsViewset, basename="clients")
router.register("projects", ProjectsViewset, basename="projects")
router.register("favours", FavoursViewset, basename="favours")
router.register("employees", EmployeesViewset, basename="employees")
router.register("project-services", ProjectServiceViewSet, basename="project-services")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("users", UserViewSet, basename="users")  # Добавили эту строку
router.register("user-profiles", UserProfileViewSet, basename="user-profiles")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', views.user_list, name='user-list'),  # Добавьте эту строку
] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
