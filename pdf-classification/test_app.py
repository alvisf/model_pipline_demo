import pytest
from app import app
client = app.test_client()


def test_something():
    url = "/"
    response = client.get(url)
    assert response.status_code == 200
