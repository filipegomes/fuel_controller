import flet as ft
from views.dashboard import Dashboard
from views.base_data_view import BaseDataView


class Router:
    def __init__(self, page):
        self.page = page
        self.routes = {
            "/": Dashboard(page),
            "/dados": BaseDataView(page)
        }
        self.body = ft.Container(content=self.routes['/'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
