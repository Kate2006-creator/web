from django.contrib import admin
from django.urls import include, path

from clients import views
from rest_framework.routers import DefaultRouter

from clients.api import ClientsViewset, ProjectsViewset, FavoursViewset, EmployeesViewset, ProjectServiceViewSet, ReviewViewSet

router = DefaultRouter()
router.register("clients", ClientsViewset, basename="clients")
router.register("projects", ProjectsViewset, basename="projects")
router.register("favours", FavoursViewset, basename="favours")
router.register("employees", FavoursViewset, basename="employees")
router.register("project-services", ProjectServiceViewSet, basename="project-services")
router.register("reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path('', views.ShowClientsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
