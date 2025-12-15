from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
   path("", views.hello, name="hello"),
   path("dashboard/", views.dashboard, name="dashboard"),
   path("submit/", views.submit_query, name="submit"),
   path("submit/success/", views.submit_success, name="submit_success"),
   path("submit_data/", views.submit_data, name="submit_data"),
]
