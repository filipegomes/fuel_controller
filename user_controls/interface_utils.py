import flet as ft
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

def create_initial_cards(value_text, title, type_card="neutral"):
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