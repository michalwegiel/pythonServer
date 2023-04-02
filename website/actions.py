from python_server.utils import Redirect
from website.views import home


def recipe_form(recipe_name, ingredients, notes):
    print(recipe_name, ingredients, notes)
    return Redirect("/home")
