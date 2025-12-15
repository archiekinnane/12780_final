from django.shortcuts import render, redirect
from django.http import HttpResponse


from weather.models import WeatherQuery, Location, StatusEnum, MetricEnum
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.timezone import now
import openpyxl

from .forms import WeatherQueryForm, WeatherDataForm



# Create your views here.
def hello(request):
   return render(request, "home.html")

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
                  

def submit_query(request):
    if request.method == "POST":
        form = WeatherQueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather:submit_success")
    else:
        form = WeatherQueryForm()

    return render(request, "weather/submit.html", {"form": form})

def submit_success(request):
    return render(request, "weather/submit_success.html")

def submit_data(request):
    if request.method == "POST":
        form = WeatherDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather:submit_success")
    else:
        form = WeatherDataForm()

    return render(request, "weather/submit_data.html", {"form": form})

def export_page(request):
    queries = WeatherQuery.objects.select_related("location").order_by(
        "location__name", "metric", "target_year"
    )

    return render(request, "weather/export.html", {
        "queries": queries
    })

def export_xlsx(request):
    qs = WeatherQuery.objects.select_related("location").all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Weather Data"

    # Header row
    ws.append(["Location","Metric", "Target Year","Baseline Start", "Baseline End",
        "Target Value","Baseline Avg", "Delta","Status",
    ])

    for q in qs:
        ws.append([
            q.location.name,
            q.get_metric_display(),
            q.target_year,
            q.baseline_start_year,
            q.baseline_end_year,
            q.target_value,
            q.baseline_avg_value,
            q.delta_value,
            q.get_status_display(),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="weather_data.xlsx"'

    wb.save(response)
    return response
