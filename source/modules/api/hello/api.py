from os import environ
from flask import jsonify, render_template, request
from requests import get, ConnectionError
from http import HTTPStatus
from connexion import FlaskApp
from modules.web_svc_functions.functions import get_server_port, get_server_name
from modules.local_db.db import get_greetings_data


# Service functions definition
def get_hello_status():
    connectivity_error = False
    status = "DOWN"
    try:
        call_hello = get(
            "http://{0}:{1}/api/hello".format(get_server_name(), get_server_port()),
            timeout=3,
        )
    except ConnectionError:
        connectivity_error = True

    if connectivity_error is False:
        status = "UP" if call_hello.status_code == HTTPStatus.OK else "DOWN"

    return status


# Main function for /api/health enpoint
def get_health():
    return (
        jsonify({"Hello Service Status": get_hello_status()}),
        HTTPStatus.OK,
    )


# Main function for /api/hello enpoint
def get_greeting():
    greetings = get_greetings_data()
    service_owner = (
        environ.get("SERVICE_OWNER")
        if environ.get("SERVICE_OWNER") != None
        else "default"
    )

    if service_owner in greetings:
        return greetings[service_owner], HTTPStatus.OK
    else:
        return greetings["default"], HTTPStatus.OK


# Function returns Flask app which is used in tests and the main application
def hello_api_app():
    app = FlaskApp(__name__, specification_dir="./")
    app.add_api("swagger.yml")

    @app.route("/", methods=["GET"])
    def root():
        return render_template("welcome.html", swagger_url=f"{request.url_root}api/ui")

    return app
