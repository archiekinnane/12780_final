from django.contrib import admin

# Register your models here.

from .models import Location, WeatherQuery

admin.site.register(Location)
admin.site.register(WeatherQuery)