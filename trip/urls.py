from django.urls import path
from .views import generate_trip

urlpatterns = [
    path('generate/', generate_trip),
]
