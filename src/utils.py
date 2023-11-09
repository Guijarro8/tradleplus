import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import random


DIRECTIONS_EMOJI = {
    "North": "⬆️",
    "South": "⬇️",
    "East": "➡️",
    "West": "⬅️",
    "Northeast": "↗️",
    "Northwest": "↖️",
    "Southeast": "↘️",
    "Southwest": "↙️",
}

color_dic= {'Animal Products':'#ed40f2',
            'Vegetable Products':'#f4ce0f',
            'Animal and Vegetable Bi-Products':'#edbd53',
            'Foodstuffs':'#a0d447',
            'Mineral Products':'#a53200',
            'Chemical Products':'#ed40f2',
            'Plastics and Rubbers':'#ff73ff',
            'Animal Hides':'#75f1b4',
            'Wood Products':'#dd0e31',
            'Paper Goods':'#efdc81',
            'Textiles':'#02a347',
            'Footwear and Headwear':'#2cba0f',
            'Stone And Glass':'#f57d41',
            'Precious Metals':'#892eff',
            'Metals':'#aa7329',
            'Machines':'#2e97ff',
            'Transportation':'#69c8ed',
            'Instruments':'#9e0071',
            'Miscellaneous':'#9c9fb2',
            'Arts and Antiques':'#847290',
            'Weapons':'#9cf2cf'}


def show_country(df_country):

    fig = px.treemap(
        df_country,
        path=["Section"], 
        # path=["Section", "HS4"], # Columna que define la jerarquía
        values="Trade Value",  # Columna que define el tamaño en porcentajes
        color="Section",  # Colores basados en la categoría 'Section'
        color_discrete_map=color_dic,  # Mapeo de colores
        title="EXPORTS OEC: 🛳️ "
            + (str(round(df_country["Trade Value"].sum() / 1e9, 2)) + " Billions" 
            if df_country["Trade Value"].sum() > 1e9
            else str(round(df_country["Trade Value"].sum() / 1e6, 2)) + " Millions"),
        labels={
            "Section": "Categoría",
            "HS4": "Nombre de la Caja",
            "Trade Value Percentage": "Porcentaje del Valor Comercial",
        },
    )

    fig.update_layout(
        width=400,  # Ancho de la figura en píxeles
        height=500,  # Alto de la figura en píxeles
    )
    return fig


def show_country_palo(df_country, name_df, random_colors):
    dic_emoji={
        "SURFACE 2019":'🌳' ,
        "DEATHS 2019": '⚰️',
        "EMIGRANTES RESIDENTES 2020":'🧳',
    }

    fig = px.treemap(
        df_country,
        path=["variable"],  # Columna que define la jerarquía
        values="value",  # Columna que define el tamaño en porcentajes
        color="variable",  # Colores basados en la categoría 'Section'
        color_discrete_sequence=random_colors,  # Mapeo de colores
        title= name_df +': ' + dic_emoji[name_df]+ ' '+ (str(round(df_country["value"].sum() / 1e9, 2)) + f"Billions"
            if df_country["value"].sum() > 1e9
            else str(round(df_country["value"].sum() / 1e6, 2)) + f"Millions"
            if df_country["value"].sum() > 1e6
            else str(round(df_country["value"].sum() / 1e3, 2)) + f"Thousands"
            if df_country["value"].sum() > 1e3
            else str(round(df_country["value"].sum(), 2))),
        # labels={'variable': 'Categoría', 'value': 'Valor'}
    )

    fig.update_layout(
        width=400,  # Ancho de la figura en píxeles
        height=500,  # Alto de la figura en píxeles
    )
    return fig


def random_color():


    return f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'

def get_random_colors(length, seed=None):
    if seed:
        random.seed(seed)
    return [random_color() for _ in range(length)]

def show_piramid(df_Country):

    fontsize=2

    # Dividir la columna 'variable' en 'sexe' y 'years'
    df_Country[['sexe', 'years','nada']] = df_Country['variable'].str.split(' ', expand=True)
    df_Country=df_Country.drop(columns=['nada','variable'])


    # Crear un gráfico de barras con Plotly
    fig = go.Figure()

    # Agregar barras para cada sexo
    for sex in df_Country['sexe'].unique():
        data_sex = df_Country[df_Country['sexe'] == sex]
        fig.add_trace(go.Bar(
            x=data_sex['value'] if sex == 'Male' else -data_sex['value'],
            y=data_sex['years'],
            name=sex,
            orientation='h',
            marker=dict(color='blue' if sex == 'Male' else 'green')
        ))

    # Ajustar el diseño del gráfico
    fig.update_layout(
        title=f'''Pirámide Demográfica: 👪 {
            str(round(df_Country["value"].sum() / 1e9, 2)) + f"Billions"
            if df_Country["value"].sum() > 1e9
            else str(round(df_Country["value"].sum() / 1e6, 2)) + f"Millions"
            if df_Country["value"].sum() > 1e6
            else str(round(df_Country["value"].sum() / 1e3, 2)) + f"Thousands"
            if df_Country["value"].sum() > 1e3
            else str(round(df_Country["value"].sum(), 2))
            }''',
        xaxis_title='Población',
        yaxis_title='Grupo de Edad',
        legend=dict(title='Sexo'),
        barmode='overlay',  # Sobreponer las barras
        bargap=0.1,         # Espacio entre las barras
    )
    
    fig.update_layout(
        width=400,  # Ancho de la figura en píxeles
        height=500,  # Alto de la figura en píxeles
    )

    # Mostrar el gráfico

    return fig

def show_bar_deaths(df_Country):
    fontsize=4
    # Dividir la columna 'variable' en 'sexe' y 'years'
    df_Country[['nada', 'years']] = df_Country['variable'].str.split(' ', expand=True)
    df_Country=df_Country.drop(columns=['nada','variable'])
    # Mostrar el DataFrame resultante

    fig = go.Figure()

    # Agregar barras para cada sexo

    fig.add_trace(go.Bar(
        x=df_Country['value'],
        y=df_Country['years'],
        name='💀 Deaths',
        orientation='h',
        marker=dict(color='black')
    ))

    # Ajustar el diseño del gráfico
    fig.update_layout(
        title=f'''Deaths by age: 💀{
            str(round(df_Country["value"].sum() / 1e9, 2)) + f"Billions"
            if df_Country["value"].sum() > 1e9
            else str(round(df_Country["value"].sum() / 1e6, 2)) + f"Millions"
            if df_Country["value"].sum() > 1e6
            else str(round(df_Country["value"].sum() / 1e3, 2)) + f"Thousands"
            if df_Country["value"].sum() > 1e3
            else str(round(df_Country["value"].sum(), 2))
            }''',
        xaxis_title='Población',
        yaxis_title='Grupo de Edad',
        legend=dict(title='💀'),
        barmode='overlay',  # Sobreponer las barras
        bargap=0.1,         # Espacio entre las barras
    )
    fig.update_layout(
        width=400,  # Ancho de la figura en píxeles
        height=500,  # Alto de la figura en píxeles
    )
    return fig

