from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('website/templates'))


def home():
    template = env.get_template('home.html')
    return template.render()


def contact():
    template = env.get_template('contact.html')
    return template.render()
