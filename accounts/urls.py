from django.urls import path
from .views import registration, profile, delete_profile

urlpatterns = [
    path("registration/", registration, name="registration"),
    path("profile/", profile, name="profile"),
    path("delete/", delete_profile, name="delete_account"),
]