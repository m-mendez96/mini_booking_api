from rest_framework import serializers

from .models import Booking
from .utils import get_nz_public_holidays


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate_start_time(self, value):
        date_only = value.date()
        year = date_only.year
        holidays = get_nz_public_holidays(year)

        if date_only in holidays:
            raise serializers.ValidationError("Cannot be scheduled on NZ holidays.")
        return value
