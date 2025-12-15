import pytest
from django.urls import reverse
from weather.models import Location, WeatherQuery, StatusEnum, MetricEnum

# test each page 
@pytest.mark.django_db
def test_dashboard_loads(client):
    url = reverse("weather:dashboard")
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_export_page_loads(client):
    resp = client.get(reverse("weather:export"))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_export_xlsx_download(client):
    resp = client.get(reverse("weather:export_xlsx"))
    assert resp.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in resp["Content-Type"]
    assert "attachment;" in resp.get("Content-Disposition", "")

# test data submission and handling 
@pytest.mark.django_db
def test_submit_data_creates_completed_query(client):
    loc = Location.objects.create(name="Test City", latitude=1.0, longitude=2.0)

    payload = {
        "location": loc.id,
        "metric": MetricEnum.DAYS_ABOVE_90F.value,          
        "target_year": 2024,
        "baseline_start_year": 1991,
        "baseline_end_year": 2020,
        "target_value": 12.0,
        "baseline_avg_value": 10.0,
    }

    resp = client.post(reverse("weather:submit_data"), data=payload)
    assert resp.status_code in (200, 302)

    q = WeatherQuery.objects.get(location=loc, metric=payload["metric"]
            , target_year=payload["target_year"])
    assert q.delta_value == pytest.approx(2.0)
    assert str(q.status) == StatusEnum.COMPLETED.value