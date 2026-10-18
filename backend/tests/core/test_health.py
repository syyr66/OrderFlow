import pytest
from pytest_django.asserts import assertContains
from django.http.response import JsonResponse
from django.urls import reverse


def test_is_alive_returns_valid_response(client):
    """Test /health/live returns a valid response"""
    response = client.get(reverse('is_alive'))

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.parametrize("db_ok, redis_ok, expected_status, expected_response", [
    pytest.param(
        False, False, 503,
        {"status": "unavailable", 
         "checks": {"db": "fail", "redis": "fail"}}
    ),
    pytest.param(
        False, True, 503,
        {"status": "unavailable", 
         "checks": {"db": "fail", "redis": "ok"}}
    ),
    pytest.param(
        True, False, 503,
        {"status": "unavailable", 
         "checks": {"db": "ok", "redis": "fail"}}
    ),
    pytest.param(
        True, True, 200,
        {"status": "ready", 
         "checks": {"db": "ok", "redis": "ok"}}
    ),
])
def test_is_ready(client, mocker, db_ok, redis_ok, expected_status, expected_response):
    """
        Test /health/ready returns appropriate status 
        and data depending on db and redis state
    """
    mocker.patch('core.health.check_db', return_value=db_ok)
    mocker.patch('core.health.check_redis', return_value=redis_ok)
    
    response = client.get(reverse('is_ready'))

    assert response.status_code == expected_status
    assert response.json() == expected_response