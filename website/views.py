from functools import cache

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('website/templates'))


def home():
    template = env.get_template('home.html')
    return "text/html", template.render()


def contact():
    template = env.get_template('contact.html')
    return "text/html", template.render()


@cache
def favicon():
    with open("website/templates/favicon.ico", "rb") as file:
        return "image/x-icon", file.read()
