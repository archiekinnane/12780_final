from django.shortcuts import render
from django.http import HttpResponse

from weather.models import WeatherQuery, Location, StatusEnum, MetricEnum
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.timezone import now



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

   metric_options = list(MetricEnum.choices)
   year_options = list( WeatherQuery.objects.filter(status=StatusEnum.COMPLETED).values_list("target_year", flat=True)
                       .distinct().order_by("target_year"))
   
   selected_metric = request.GET.get("metric") or MetricEnum.DAYS_ABOVE_90F
   selected_year = request.GET.get("year")
   selected_year = int(selected_year) if selected_year and selected_year.isdigit() else year_options[-1]

   delta_qs = WeatherQuery.objects.filter(status=StatusEnum.COMPLETED, metric=selected_metric, target_year=selected_year
                                          , delta_value__isnull=False).select_related("location").order_by("-delta_value")
   
   delta_labels = [q.location.name for q in delta_qs]
   delta_values = [q.delta_value for q in delta_qs]

   

   return render(request, "weather/dashboard.html"
                 ,{"queries": data
                    , "status_labels": status_labels
                    , "status_values": status_values
                    , "time_labels": time_labels
                    , "time_values": time_values
                    ,"metric_options": metric_options
                    ,"year_options": year_options
                    ,"selected_metric": selected_metric
                    ,"selected_year": selected_year
                    ,"delta_labels": delta_labels
                    ,"delta_values": delta_values
                    })