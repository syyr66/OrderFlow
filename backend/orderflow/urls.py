from django.contrib import admin
from django.urls import path
from core.health import is_alive, is_ready

urlpatterns = [
    path('admin/', admin.site.urls),
    # Healthchecks
    path('health/live', is_alive, name='is_alive'),
    path('health/ready', is_ready, name='is_ready'),
]
