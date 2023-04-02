from website.views import home, contact, favicon

routes = {
    "/": home,
    "/home": home,
    "/contact": contact,
    "/favicon.ico": favicon,
}
