import os
from http import HTTPStatus
from modules.api.hello.api import get_greeting, get_server_port, get_server_name


def test_server_port_symbols():
    os.environ["SERVER_PORT"] = "7673fs"
    assert get_server_port() == 8080


def test_server_port_numbers():
    os.environ["SERVER_PORT"] = "7233"
    assert get_server_port() == 7233


def test_server_port_large_numbers():
    os.environ["SERVER_PORT"] = "87233"
    assert get_server_port() == 8080


def test_server_port_small_numbers():
    os.environ["SERVER_PORT"] = "665"
    assert get_server_port() == 8080


def test_server_port_novar():
    assert get_server_port() == 8080


def test_server_name():
    assert get_server_name() == "localhost"


def test_greetings_customerB():
    os.environ["SERVICE_OWNER"] = "customerB"
    assert get_greeting() == ("Dear Sir or Madam", HTTPStatus.OK)


def test_greetings_non_existed_owner():
    os.environ["SERVICE_OWNER"] = "customerF"
    assert get_greeting() == ("Hello", HTTPStatus.OK)
