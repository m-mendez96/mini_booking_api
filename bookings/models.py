from django.conf import settings
from django.db import models


class Booking(models.Model):
    farm_name = models.CharField(max_length=255)
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    temperature = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm_name} - {self.start_time}"
