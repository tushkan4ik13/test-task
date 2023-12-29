from modules.api.hello.api import hello_api_app
from modules.local_db.db import get_greetings_data


def test_home_page():
    flask_app = hello_api_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert "Welcome to API Hello Service" in response.text


def test_hello_endpoint():
    flask_app = hello_api_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/api/hello")
        assert response.status_code == 200
        assert response.text in get_greetings_data().values()


def test_health_endpoint():
    flask_app = hello_api_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/api/health")
        assert response.status_code == 200
        assert "Hello Service Status" in response.text
