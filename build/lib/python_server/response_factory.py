from website.routes import routes


def response_factory_get(route):
    content = routes.get(route, None)
    if content:
        return 200, "OK", content()
    with open("python_server/pages/page_not_found.html", "r") as html_file:
        content = html_file.read()
    return 404, "PAGE NOT FOUND", content
