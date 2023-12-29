"""
Various service and help functions, which are used in the project
"""


from os import environ


def get_server_port():
    port = default_port = 8080
    server_port_env_var = environ.get("SERVER_PORT")
    if server_port_env_var != None and server_port_env_var.isnumeric():
        # Based on https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
        if int(server_port_env_var) >= 1024 and int(server_port_env_var) <= 65535:
            port = int(server_port_env_var)
            print(
                f"Using SERVER_PORT environment variable to set web server port. Server port is {port}"
            )
        else:
            print(
                f"Provided network port in SERVER_PORT environment variable is out of range 1024-65535. Set default port - {default_port}"
            )
    else:
        print(
            f"SERVER_PORT environment variable isn't defined or contains non-numeric symbols. Set default port - {default_port}"
        )

    return port


# Mock function to generate hostname
def get_server_name():
    return "localhost"
