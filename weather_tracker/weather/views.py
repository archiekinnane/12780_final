from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request):
   return HttpResponse("Hello World from Hyperlocal Weather Tracker App!")

def dashboard(request):
   return HttpResponse("Dashboard works")