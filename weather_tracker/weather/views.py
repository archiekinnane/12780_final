from django.shortcuts import render
from django.http import HttpResponse

from weather.models import WeatherQuery, Location, StatusEnum, MetricEnum

from django.db.models import Count

from django.db.models.functions import TruncDate



# Create your views here.
def hello(request):
   return HttpResponse("Hello World from Hyperlocal Weather Tracker App!")

def dashboard(request):
   data = WeatherQuery.objects.all()
   pending_count = data.filter(status=StatusEnum.PENDING).count()
   completed_count = data.filter(status=StatusEnum.COMPLETED).count()
   failed_count = data.filter(status=StatusEnum.FAILED).count()

   status_labels = ["Pending", "Completed", "Failed"]
   status_values = [pending_count, completed_count, failed_count]
   
   stats = WeatherQuery.objects.annotate(date=TruncDate('created_at')) \
                       .values('date') \
                       .annotate(count=Count('id')) \
                       .order_by('date')
   
   time_labels = [row["date"].isoformat() for row in stats]
   
   time_values = [row["count"] for row in stats]

   return render(request, "weather/dashboard.html"
                 , {"queries": data, "status_labels": status_labels, "status_values": status_values, "time_labels": time_labels, "time_values": time_values
                    })