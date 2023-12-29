from modules.api.hello.api import hello_api_app
from modules.web_svc_functions.functions import get_server_port


# Start web server
app = hello_api_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=get_server_port(), lifespan="off", log_level="info")
