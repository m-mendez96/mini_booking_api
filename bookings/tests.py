from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from bookings.models import Booking

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post(
        reverse("token_obtain_pair"),
        {"username": user.username, "password": "testpass"},
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.mark.django_db
def test_create_booking_valid(auth_client, user):
    url = reverse("booking-list")
    data = {
        "farm_name": "Granja Verde",
        "inspector": user.id,
        "start_time": (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z",
        "duration_minutes": 60,
        "notes": "Inspección general",
        "latitude": -41.2,
        "longitude": 174.7,
    }

    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_create_booking_in_the_past(auth_client, user):
    url = reverse("booking-list")
    data = {
        "farm_name": "Farm Test",
        "inspector": user.id,
        "start_time": (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z",
        "duration_minutes": 60,
        "notes": "Past Date",
        "latitude": -41.2,
        "longitude": 174.7,
    }

    response = auth_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "Start time must be in the future." in str(response.data)


@pytest.mark.django_db
def test_create_booking_on_holiday(auth_client, user):
    url = reverse("booking-list")
    data = {
        "farm_name": "Farm Test",
        "inspector": user.id,
        "start_time": "2026-01-01T10:00:00Z",
        "duration_minutes": 60,
        "notes": "Holiday",
        "latitude": -41.2,
        "longitude": 174.7,
    }

    response = auth_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "Cannot be scheduled on NZ holidays." in str(response.data)
