import json

import requests

# Use for local testing
API_URL = "http://127.0.0.1:8888"


def test_healthcheck():
    response = requests.get(f"{API_URL}/healthcheck")
    assert bool(response.json()["healthcheck"]) == True


def test_insert():
    response = requests.post(
        f"{API_URL}/insert",
        data=json.dumps(["author", "title", "description", "url", "pub_date"]),
    )
    assert response.status_code == 200


def test_get_news():
    response = requests.get(f"{API_URL}/news")
    assert response.status_code == 200


def test_purge():
    response = requests.get(f"{API_URL}/purge")
    assert response.status_code == 200


if __name__ == "__main__":
    pass
