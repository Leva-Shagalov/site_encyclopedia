from django.urls import path
from .views import registration, profile

urlpatterns = [
    path("registration", registration, name="registration"),
    path("profile", profile, name="profile")
]