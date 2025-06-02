from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('themes.urls')),  # Add themes URLs
] 