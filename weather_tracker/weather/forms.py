from django import forms
from .models import WeatherQuery, StatusEnum

class WeatherQueryForm(forms.ModelForm):
    class Meta:
        model = WeatherQuery
        fields = [
            "location",
            "metric",
            "target_year",
            "baseline_start_year",
            "baseline_end_year",
        ]

class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherQuery
        fields = [
            "location",
            "metric",
            "target_year",
            "baseline_start_year",
            "baseline_end_year",
            "target_value",
            "baseline_avg_value",
        ]

    def save(self, commit=True):
        obj = super().save(commit=False)

        obj.delta_value = obj.target_value - obj.baseline_avg_value
        obj.status = StatusEnum.COMPLETED   # must match your model's choices exactly

        if commit:
            obj.save()
        return obj