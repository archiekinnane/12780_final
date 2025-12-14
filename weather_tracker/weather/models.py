from django.db import models

# Create your models here.

class StatusEnum(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"

class MetricEnum(models.TextChoices):
    DAYS_ABOVE_90F = "days_above_90f", "Days Above 90F"
    DAYS_BELOW_32F = "days_below_32f", "Days Below 32F"

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class WeatherQuery(models.Model):
    #inputs 
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    metric = models.CharField(
        max_length=30,
        choices=MetricEnum.choices,
    )
    target_year = models.IntegerField()
    baseline_start_year = models.IntegerField()
    baseline_end_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    #outputs
    target_value = models.FloatField(null=True, blank=True)
    baseline_avg_value = models.FloatField(null=True, blank=True)
    delta_value = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusEnum.choices,
        default=StatusEnum.PENDING,
    )    
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.metric} at {self.location.name} in {self.target_year}"