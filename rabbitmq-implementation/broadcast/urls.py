from django.urls import path
from .views import broadcast_view

urlpatterns = [
    path("", broadcast_view, name="broadcast"),
]
