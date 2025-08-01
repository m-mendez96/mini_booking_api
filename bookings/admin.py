from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("farm_name", "inspector", "start_time", "duration_minutes")
    search_fields = ("farm_name", "inspector__username")
    list_filter = ("start_time",)
