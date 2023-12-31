from flet import *
import flet as ft
from views.dashboard import Dashboard
from views.base_data_view import BaseDataView
from user_controls.nav_controls import nav_bar_handler, nav_drawer_handler
from user_controls.nav_router import Router
from auth import *



def main(page: Page):


    page.title = "Fuel Control CMJG"
    page.padding = 10
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.alignment = ft.MainAxisAlignment.CENTER
    page.spacing = 15
    #page.theme = theme.Theme(color_scheme_seed="blue")
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE,
            primary_container=ft.colors.BLUE_200,
            secondary=ft.colors.BLUE_400,
            # ...
        ),
    )

    if page.client_storage.contains_key("tema") is False:
        page.client_storage.set("tema", "light")
    else:
        page.theme_mode = page.client_storage.get("tema")

    def window_event(e):
        if page.window_maximized == True:
            page.client_storage.set("window",True)
        else:
            page.client_storage.set("window",False)
    page.on_window_event = window_event
    page.window_maximized = page.client_storage.get("window")

    page.margin = margin.all(15)
    page.navigation_bar = nav_bar_handler(page)
    page.drawer = nav_drawer_handler(page)
    my_router = Router(page)
    page.on_route_change = my_router.route_change



    page.update()

    page.add(
        ft.Column(controls=[
            ft.Column(
                controls=[
                    my_router.body,
                ],
                expand=True,
            )
        ]
        )
    )


#app(target=main, assets_dir='assets', upload_dir='assets/uploads', view=WEB_BROWSER, port=8550)
app(target=main, assets_dir='assets')
