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


class Dashboard(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.content = None
        self.page = page

    def build(self):
        # url: str = SUPABASE_URL
        # key: str = SUPABASE_KEY
        # supabase: Client = create_client(url, key)
        response = supabase.table('data_cars').select("*").execute()
        # -------> MAIN COLUMN <--------- #
        main_column = ft.Column()

        # --------> VARIABLES *INITIAL CARDS* ROW <---------#
        initial_cards_row = ft.ResponsiveRow()
        budget_value = 76600  # put that on settings
        fuel_total_text = ft.Text("Envie o arquivo.")
        irregular_text = ft.Text("Envie o arquivo.")
        budget_text = ft.Text(number_formatter(format(budget_value, '.2f')))

        # --------> VARIABLES *SEND_FILE* ROW <---------#
        name_file_field = ft.TextField(label="Nome do Arquivo:", read_only=True, value="", col=3)
        qtd_lines = ft.TextField(label="Linhas:", read_only=True, value="", col=1)
        initial_date_field = ft.TextField(label="Data Inicial:", read_only=True, value="", col=2)
        final_date_field = ft.TextField(label="Data Final:", read_only=True, value="", col=2)
        total_value_field = ft.TextField(label="Valor Total:", read_only=True, value="", col=2)

        send_file_button = ft.ElevatedButton(
            "Envie o Arquivo",
            icon=ft.icons.UPLOAD_FILE_ROUNDED,
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            height=60,
            on_click=lambda _: pick_file.pick_files(allowed_extensions=["csv", "txt"]),
            col=2
        )

        # Stylizing TextFields with utils.text_fields_config:
        text_fields_config(name_file_field, qtd_lines, initial_date_field, final_date_field, total_value_field)

        file_data_upload = ft.ResponsiveRow(
            controls=[
                send_file_button,
                name_file_field,
                qtd_lines,
                total_value_field,
                initial_date_field,
                final_date_field,
            ],
        )
        # --------> VARIABLES *TABLE INPUT* CONTAINER <---------#
        table_data_input = ft.DataTable()
        data_fuel_df = pd.DataFrame()

        # --------> VARIABLES *TABLE OUTPUT* CONTAINER <---------#
        table_data_output = ft.DataTable()

        # ---------> FUNCTIONS:

        def create_cards(value_text, title, type_card):
            """
            :param value_text: um objeto ft.Text() com o valor a ser impresso.
            :param title: título do card.
            :param type_card: tipo do card (positive[verde], negative[vermelho], neutral[cor padrão])
            :return: um card pronto com as informações e cores informadas.
            """

            if type_card == "positive":
                card_type = {
                    'icon': ft.icons.ATTACH_MONEY_ROUNDED,
                    'color': ft.colors.GREEN,
                    'bgcolor': ft.colors.GREEN_200
                }
            elif type_card == "negative":
                card_type = {
                    'icon': ft.icons.MONEY_OFF_ROUNDED,
                    'color': ft.colors.RED,
                    'bgcolor': ft.colors.RED_200
                }
            else:
                card_type = {
                    'icon': ft.icons.WALLET_ROUNDED,
                    'color': ft.colors.ON_PRIMARY,
                    'bgcolor': ft.colors.PRIMARY
                }

            value_text.style = ft.TextThemeStyle.DISPLAY_SMALL
            value_text.text_align = ft.TextAlign.START
            value_text.color = card_type['bgcolor']

            card = ft.Card(
                content=ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=Icon(card_type['icon'], color=card_type['color'], size=48),
                                        bgcolor=card_type['bgcolor'],
                                        alignment=ft.alignment.center,
                                        shape=ft.BoxShape.CIRCLE,
                                    ),
                                    ft.Text(
                                        value=f"{title.upper()}",
                                        style=ft.TextThemeStyle.TITLE_SMALL,
                                        color=card_type['bgcolor']
                                    ),
                                ],
                                col=4,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),

                            ft.Column(
                                controls=[
                                    ft.ListTile(
                                        title=value_text,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER, col=8)
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    ),
                    width=400,
                    padding=10,
                ),
                col=4,
                surface_tint_color=card_type['bgcolor'], elevation=5.0
            )
            return card

        def file_upload(e: FilePickerResultEvent):
            """
            :param e: FilePickerResultEvent
            :return: Uploaded file.
            """

            if e.files is not None:
                # # -------> LOADING ANIMATION
                animation_loading(self.page, send_file_button, 1)
                # # <--------- LOADING ANIMATION

                self.page.session.set("uploaded_file", str(e.files[0].path))

                data_fuel, total, initial_date, final_date = utils_read_file(str(e.files[0].path))
                data_fuel.to_json('data/data_fuel.json')

                data_fuel_cropped = utils_read_file(str(e.files[0].path), True)
                data_fuel_cropped.to_json('data/data_fuel_cropped.json')

                # --> Updating TextFields information:
                name_file_field.value = e.files[0].name
                total_value_field.value = total.replace('.', ',')
                initial_date_field.value = initial_date
                final_date_field.value = final_date

                qtd_lines.value = str(len(data_fuel.index))
                file_data_upload.update()

                # --> Updating INITIAL CARDS information:
                fuel_total_text.value = number_formatter(total)
                budget_text.value = number_formatter(format(float(budget_value) - float(total), '.2f'))
                initial_cards_row.update()

                card_data_table_input = data_table(data_fuel_cropped)
                if len(main_column.controls) > 2:
                    main_column.controls.pop(2)
                    main_column.controls[2] = card_data_table_input
                else:
                    main_column.controls.append(card_data_table_input)

                card_data_table_output = verify_irregular()
                if len(main_column.controls) > 3:
                    main_column.controls.pop(3)
                    main_column.controls[3] = card_data_table_output
                else:
                    main_column.controls.append(card_data_table_output)

                main_column.update()



        card_file = ft.Card(
            content=ft.Column(
                controls=[
                    ft.Container(
                        ft.ListTile(
                            title=ft.Text(f"Envie a Planilha Mensal de Abastecimentos",
                                          style=ft.TextThemeStyle.HEADLINE_SMALL,
                                          text_align=ft.TextAlign.CENTER),
                            subtitle=ft.Text(
                                "Envie a planilha mensal de abastecimentos em formato CSV. Os campos abaixo serão automaticamente preenchidos.",
                                text_align=ft.TextAlign.CENTER,
                                style=ft.TextThemeStyle.BODY_SMALL)
                        ),
                    ),
                    ft.Container(
                        content=file_data_upload,
                        padding=ft.padding.only(10, 0, 10, 10),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
            )
        )

        def data_table(dataframe):
            data_fuel_df = pd.read_json('data/data_fuel.json')
            data_fuel_cropped = pd.read_json('data/data_fuel_cropped.json')

            table_data_input.columns = return_headers(data_fuel_cropped)
            table_data_input.rows = return_rows(data_fuel_cropped)
            table_data_input.expand = True

            table_data_input_listview = ft.ListView(expand=1, spacing=1, padding=10, height=200)
            table_data_input_listview.controls.append(table_data_input)
            print(list(table_data_input.columns))

            card_data_table = ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.ListTile(
                                title=ft.Text(f"Envie a Planilha Mensal de Abastecimentos",
                                              style=ft.TextThemeStyle.HEADLINE_SMALL,
                                              text_align=ft.TextAlign.CENTER),
                                subtitle=ft.Text(
                                    "Envie a planilha mensal de abastecimentos em formato CSV. Os campos abaixo serão automaticamente preenchidos.",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextThemeStyle.BODY_SMALL)
                            ), padding=ft.padding.only(10, 5, 10, 0)
                        ),
                        ft.Container(
                            content=table_data_input_listview,
                            padding=ft.padding.only(10, 0, 10, 5),
                            alignment=ft.alignment.center,
                        ),

                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
                )
            )

            return card_data_table


        def verify_irregular():

            data_cars = pd.read_json('data/data_cars.json')
            data_fuel_df = pd.read_json('data/data_fuel.json')
            data_fuel_cropped = pd.read_json('data/data_fuel_cropped.json')

            table_data_output.columns = return_headers(data_cars)
            table_data_output.rows = return_rows(data_cars)
            table_data_output.expand = True

            table_data_output_listview = ft.ListView(expand=1, spacing=1, padding=10, height=200)
            table_data_output_listview.controls.append(table_data_output)
            print(list(table_data_output.columns))

            card_output_table = ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.ListTile(
                                title=ft.Text(f"Envie a Planilha Mensal de Abastecimentos",
                                              style=ft.TextThemeStyle.HEADLINE_SMALL,
                                              text_align=ft.TextAlign.CENTER),
                                subtitle=ft.Text(
                                    "Envie a planilha mensal de abastecimentos em formato CSV. Os campos abaixo serão automaticamente preenchidos.",
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextThemeStyle.BODY_SMALL)
                            ), padding=ft.padding.only(10, 5, 10, 0)
                        ),
                        ft.Container(
                            content=table_data_output_listview,
                            padding=ft.padding.only(10, 0, 10, 5),
                            alignment=ft.alignment.center,
                        ),

                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
                )
            )

            return card_output_table

        fuel_total_card = create_cards(fuel_total_text, "Total Gasto", "positive")
        irregular_card = create_cards(irregular_text, "Total Irregular", "negative")
        budget_card = create_cards(budget_text, "Saldo", "neutral")

        initial_cards_row = ft.ResponsiveRow(
            controls=[
                fuel_total_card,
                irregular_card,
                budget_card
            ]
        )

        # Statements for File Picker:
        pick_file = FilePicker(on_result=file_upload)
        self.page.overlay.append(pick_file)

        main_column.controls = [
            initial_cards_row,
            card_file,
        ]

        self.content = [
            main_column
        ]
        return self.content
