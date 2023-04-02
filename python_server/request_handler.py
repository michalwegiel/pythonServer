from python_server.http_response import HTTPResponse, HTTPResponseCode
from python_server.response_factory import response_factory_get


def handle_request(request: bytes) -> bytes:
    """
    Process an incoming HTTP request and return an HTTP response.

    Args:
        request (bytes): The HTTP request as a bytes object.

    Returns:
        bytes: The HTTP response as a bytes object.
    """
    # Split the request into lines and extract the request method and route.
    lines = request.splitlines()
    request_method_header, *payload = lines
    request_method, route, _ = request_method_header.split(b" ")

    # Use a match statement to determine the appropriate response based on the request method.
    match request_method:
        case b"GET":
            # Call the response_factory_get() function with the route parameter.
            status_code, status_info, content_type, content = response_factory_get(
                route=route.decode()
            )
        case _:
            # Read the contents of the "bad_request.html" file and set the status code and status information.
            with open(
                "python_server/pages/bad_request.html", "r", encoding="UTF-8"
            ) as html_file:
                status_code, status_info, content_type, content = (
                    HTTPResponseCode.BAD_REQUEST,
                    "text/html",
                    "BAD REQUEST",
                    html_file.read(),
                )

    # Create an HTTPResponse object and return the result of calling the produce_response() method.
    return HTTPResponse(
        status_code=status_code,
        status_info=status_info,
        content_type=content_type,
        content=content,
    ).produce_response()
