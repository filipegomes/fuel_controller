from flet import (
    Container,
    UserControl,
    Icon,
    Page,
    Text,
    AppBar,
    PopupMenuButton,
    PopupMenuItem,
    colors,
    icons,
    margin,

)
import flet as ft
from user_controls.utils import *
from auth import supabase
from user_controls.interface_utils import *


class BaseDataView(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        main_column = ft.Column()

        initial_cards_row = ft.ResponsiveRow()
        active_cars_text = ft.Text("Envie o arquivo.")
        inactive_cars_text = ft.Text("Envie o arquivo.")

        active_cars_card = create_initial_cards(active_cars_text, "Carros Ativos", "positive")
        inactive_cars_card = create_initial_cards(inactive_cars_text, "Carros Inativos", "negative")

        initial_cards_row.controls = [
            active_cars_card,
            inactive_cars_card
        ]

        main_column.controls = [
            initial_cards_row
        ]

        content = [
            main_column
        ]
        return content
