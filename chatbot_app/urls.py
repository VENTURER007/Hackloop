from . import views
from django.urls import path
print("Loading")
urlpatterns = [
    path("",views.ai)
    ]

