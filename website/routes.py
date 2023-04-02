from website.views import home, contact, favicon
from website.actions import recipe_form

routes = {
    "/": home,
    "/home": home,
    "/contact": contact,
    "/favicon.ico": favicon,
}

actions = {
    "/recipe_form": recipe_form,
}
