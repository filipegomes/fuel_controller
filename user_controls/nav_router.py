import flet as ft

from views.dashboard import Dashboard


class Router:
    def __init__(self, page):
        self.page = page
        self.ft = ft
        self.routes = {
            "/": Dashboard(page),
            #"/settings": settings_view(page)
        }
        self.body = ft.Container(content=self.routes['/'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
