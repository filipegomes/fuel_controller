import flet as ft
from flet import *


def nav_bar_handler(page: Page):

    def theme_changed(e):
        if page.theme_mode == "dark":
            page.client_storage.set("tema", "light")
            page.update()
        else:
            page.client_storage.set("tema", "dark")
            page.update()
        page.theme_mode = page.client_storage.get("tema")
        page.update()

    def show_drawer(e):
        page.drawer.open = True
        page.drawer.update()

    nav_bar = ft.AppBar(
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        leading_width=40,
        title=ft.Text("Análise de Combustível da CMJG", color=ft.colors.ON_PRIMARY_CONTAINER, style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        center_title=True,
        bgcolor=ft.colors.PRIMARY,
        actions=[
            ft.IconButton(icon=ft.icons.BRIGHTNESS_4_OUTLINED, on_click=theme_changed),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False
                    ),
                ]
            ),
        ],
    )
    return nav_bar


def nav_drawer_handler(page: Page):
    nav_drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )
    return nav_drawer
