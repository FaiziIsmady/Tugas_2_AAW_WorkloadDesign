from django.urls import path
from .views import broadcast_view, consumer_dashboard_view

urlpatterns = [
    path("", broadcast_view, name="broadcast"),
    path("consumer/", consumer_dashboard_view, name="consumer-dashboard"),
]
