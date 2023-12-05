import pandas as pd
import numpy as np
import flet as ft
from time import sleep
import re


# def create_assets_directory(page: object) -> object:
#     path = os.path.join(os.getcwd(), "data_assets")
#     # # check whether directory already exists
#     if not os.path.exists(path):
#         os.mkdir(path)
#         print("Folder %s created!" % path)
#         page.client_storage.set("update_codes", True)
#     else:
#         page.client_storage.set("update_codes", False)
#         print("Folder %s already exists" % path)


def animation_loading(page, button, time):
    page.splash = ft.ProgressBar()
    button.disabled = True
    page.update()
    sleep(time)
    page.splash = None
    button.disabled = False
    page.update()


def text_fields_config(*text_fields):
    for field in text_fields:
        field.border_radius = ft.border_radius.all(10)
        field.border_color = ft.colors.PRIMARY_CONTAINER
        field.focused_border_color = ft.colors.PRIMARY
        field.text_align = ft.TextAlign.CENTER

    return text_fields


def read_grades(file_name):
    # grades = pd.read_csv(file_name+".tsv", sep=sep, index_col=0, decimal=decimal)
    grades = pd.read_excel(file_name)
    grades.rename(columns={'Unnamed: 0': 'Matricula'}, inplace=True)
    grades = grades.astype({"Matricula": str})
    grades['Matricula'] = grades['Matricula'].str.removesuffix('.0')
    grades = grades.set_index('Matricula')

    try:
        grades_courses = dict(grades.iloc[0][2:-1].str.replace('Peso ', ''))
    except AttributeError:
        grades_courses = dict(grades.iloc[0][2:-1])

    grades_courses.update((k, float(v)) for k, v in grades_courses.items())
    grades = grades.drop('nan', axis=0)
    for item in grades_courses.keys():
        grades[item] = pd.to_numeric(grades[item], errors='coerce')
    return grades, grades_courses


def utils_read_file(file_name):
    data_fuel = pd.read_csv(file_name, sep=";", decimal=',', parse_dates=True, header=1,
                            index_col=0)  # O arquivo de entrada precisa estar com as casas decimais delimitadas por vírgula.
    data_fuel.drop([
        "Unidade",
        "Subunidade",
        "Prefixo",
        "Veículo Provisório",
        "Registro",
        "Valor Considerado",
        "Valor Liquido",
        "Km",
        "KML",
        "KM Rodado",
        "Intervalo",
        "Simples Nacional",
        "Tipo Condutor",
        "Unidade Condutor",
        "Subunidade Condutor",
        "Unnamed: 30"],
        axis="columns",
        inplace=True)

    data_fuel.dropna(thresh=2, inplace=True)
    data_fuel['Data/Hora'] = pd.to_datetime(data_fuel['Data/Hora'], dayfirst=True, format="%d/%m/%Y %H:%M:%S")
    data_fuel['Cartão'] = data_fuel['Cartão'].apply(lambda x: format(float(x), ".0f")).astype(str)

    data_fuel.index.names = ['cod_trans']
    data_fuel.rename(columns={
        'Data/Hora': 'datetime',
        'Placa': 'car_register_number',
        'Ano Veículo': 'car_year_model',
        'Cartão': 'card_number',
        'Combustível/Serviço': 'trans_fuel_type',
        'Condutor': 'driver_name',
        'Estabelecimento': 'location_name',
        'Cidade': 'location_city',
        'UF': 'location_UF',
        'CNPJ': 'cod_cnpj',
        'Qtde (L)': 'trans_fuel_qtd',
        'Preco Unitário': 'trans_fuel_price',
        'Valor Bruto': 'trans_fuel_total',
        'Tipo de Venda': 'trans_type',
    }, inplace=True)
    data_fuel['car_register_number'] = data_fuel['car_register_number'].str.replace('-', '')

    total_value = format(data_fuel['trans_fuel_total'].sum(), '.2f')

    first_date = data_fuel['datetime'].min().date()
    first_date = f"{first_date.day} / {first_date.month} / {first_date.year}"

    last_date = data_fuel['datetime'].max().date()
    last_date = f"{last_date.day} / {last_date.month} / {last_date.year}"

    return data_fuel, total_value, first_date, last_date


def return_headers(df: pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]


def return_rows(df: pd.DataFrame) -> list:
    rows = []
    for index, row in df.iterrows():
        rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows


def dialog_standard(page, title, content, button_text):
    def close_dlg(e):
        dlg_aviso.open = False
        page.update()

    dlg_aviso = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, text_align=ft.TextAlign.CENTER),
        content=ft.Text(content, text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton(button_text, on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        on_dismiss=lambda e: print("Modal dialog dismissed!"), )
    page.dialog = dlg_aviso
    dlg_aviso.open = True
    page.update()


def number_formatter(value, thou=".", dec=","):
    """
    :param value: string to be transformed.
    :param thou: a thousand separator.
    :param dec: decimal/fraction separator.
    :return: transformed string with the format 1.000,00
    """
    integer, decimal = value.split(".")
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)

    return "R$ " + integer + dec + decimal
