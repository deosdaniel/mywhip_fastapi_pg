from http.client import responses
import pytest
from fastapi import status


BASE_URL = "/api/v1/cars"


def test_get_all_cars(test_client):
    response = test_client.get(f"{BASE_URL}/5cca3ffe-4576-4a53-9dc4-ef6e43dcbf63")
    assert response.status_code == status.HTTP_200_OK
