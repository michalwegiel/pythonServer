from functools import cache
from urllib.parse import parse_qs
from python_server.http_response import HTTPResponse, HTTPResponseCode, HTTPResponseRedirect
from python_server.utils import Redirect
from website.routes import routes, actions


@cache
def page_not_found():
    with open("python_server/pages/page_not_found.html", "r", encoding="UTF-8") as html_file:
        content = html_file.read()
    return HTTPResponse(status_code=HTTPResponseCode.NOT_FOUND, status_info="PAGE NOT FOUND", content_type="text/html", content=content)


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
        return HTTPResponse(status_code=HTTPResponseCode.OK, status_info="OK", content_type=content_type, content=content)
    return page_not_found()


def response_factory_post(action: str, data: str):
    parsed_data = {k.replace("-", "_"): v[0] for k, v in parse_qs(qs=data, keep_blank_values=True).items()}
    action = actions.get(action, None)
    if action is not None:
        action_result = action(**parsed_data)  # type: ignore
        if isinstance(action_result, Redirect):
            location = action_result.location
            return HTTPResponseRedirect(location=location)
        content_type, content = action_result
        return HTTPResponse(status_code=HTTPResponseCode.OK, status_info="OK", content_type=content_type, content=content)
    return page_not_found()
