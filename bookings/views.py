from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer
from .utils import get_current_weather


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            weather = get_current_weather(instance.latitude, instance.longitude)
            instance.temperature = weather["temperature"]
            instance.wind_speed = weather["wind_speed"]
            instance.save()
        except Exception:
            pass

    def perform_update(self, serializer):
        instance = serializer.save()
        try:
            weather = get_current_weather(instance.latitude, instance.longitude)
            instance.temperature = weather["temperature"]
            instance.wind_speed = weather["wind_speed"]
            instance.save()
        except Exception:
            pass
