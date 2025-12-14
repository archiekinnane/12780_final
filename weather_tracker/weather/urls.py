from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
   path("", views.hello, name="hello"),
   path("dashboard/", views.dashboard, name="dashboard"),
]
