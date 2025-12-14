from django.shortcuts import render
from django.http import HttpResponse

from weather.models import WeatherQuery

# Create your views here.
def hello(request):
   return HttpResponse("Hello World from Hyperlocal Weather Tracker App!")

def dashboard(request):
   data = WeatherQuery.objects.all()
   return render(request, "weather/dashboard.html", {"queries": data})