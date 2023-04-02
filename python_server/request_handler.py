from python_server.http_response import HTTPResponse, HTTPResponseCode
from python_server.response_factory import response_factory_get, response_factory_post


def handle_request(request: bytes) -> bytes:
    """
    Process an incoming HTTP request and return an HTTP response.

    Args:
        request (bytes): The HTTP request as a bytes object.

    Returns:
        bytes: The HTTP response as a bytes object.
    """
    # Split the request into lines and extract the request method and route.
    lines: list[bytes]
    request_method_header: bytes
    payload: list[bytes]
    request_method: bytes
    route: bytes

    lines = request.splitlines()
    request_method_header, *payload = lines
    request_method, route, _ = request_method_header.split(b" ")

    decoded_route: str = route.decode()
    match request_method:
        case b"GET":
            # Call the response_factory_get() function with the route parameter.
            response = response_factory_get(route=decoded_route)
        case b"POST":
            data = payload.pop().decode()
            response = response_factory_post(action=decoded_route, data=data)
        case _:
            # Read the contents of the "bad_request.html" file and set the status code and status information.
            with open("python_server/pages/bad_request.html", "r", encoding="UTF-8") as html_file:
                status_code, status_info, content_type, content = (
                    HTTPResponseCode.BAD_REQUEST,
                    "text/html",
                    "BAD REQUEST",
                    html_file.read(),
                )
            response = HTTPResponse(
                status_code=status_code,
                status_info=status_info,
                content_type=content_type,
                content=content,
            )

    return response.produce_response()
