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
from flet_core import FilePicker, FilePickerResultEvent
from user_controls.utils import *
# from auth import SUPABASE_URL,SUPABASE_KEY
# from supabase import create_client, Client
from auth import supabase


class BaseDataView(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.content = None
        self.page = page

    def build(self):
        main_column = ft.Column()

        main_column.controls = [

        ]

        self.content = [
            main_column
        ]
        return self.content
