from python_server.http_response import HTTPResponseCode
from website.routes import routes


def response_factory_get(route: str):
    """Returns an HTTP response tuple based on the specified route.

    Args:
        route: The HTTP route to generate a response for.

    Returns:
        A tuple containing an HTTP status code, a status message, and response content.

    """
    view = routes.get(route, None)
    if view is not None:
        content_type, content = view()  # type: ignore
        return HTTPResponseCode.OK, "OK", content_type, content
    with open(
        "python_server/pages/page_not_found.html", "r", encoding="UTF-8"
    ) as html_file:
        content_type, content = "text/html", html_file.read()
    return HTTPResponseCode.NOT_FOUND, "PAGE NOT FOUND", content_type, content
