from python_server.http_response import HTTPResponse
from python_server.response_factory import response_factory_get


def handle_request(request: bytes):
    lines = request.splitlines()
    request_method_header, *payload = lines
    request_method, route, _ = request_method_header.split(b" ")

    match request_method:
        case b"GET":
            status_code, status_info, content = response_factory_get(
                route=route.decode()
            )
        case _:
            with open("python_server/pages/bad_request.html", "r") as html_file:
                status_code, status_info, content = 400, "Bad request", html_file.read()

    return HTTPResponse(
        status_code=status_code, status_info=status_info, content=content
    ).produce_response()
