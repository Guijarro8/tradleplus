import pandas
import random
import streamlit as st

from datetime import datetime

from src.utils import DIRECTIONS_EMOJI,show_piramid ,show_country,show_bar_deaths, show_country_palo, get_random_colors

#################################################
# Wallpaper
#################################################
background_image = "picture/wallpaper.jpg"
# import base64

# @st.cache_data()
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = '''
#     <style>
#     body {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
    
#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_png_as_page_bg('picture/wallpaper.jpg')
st.title("Tradle plus")

#################################################
##LOAD DATA
#################################################

countries_direction_df = pandas.read_csv("data/countries_direction.csv", index_col=0)
countries_distances_df = pandas.read_csv("data/countries_distances.csv", index_col=0)
# Get the current date as an integer (e.g., 20231104 for November 4, 2023)
current_date = int(datetime.now().strftime("%Y%m%d"))
random.seed(current_date)
# Create a dictionary to map the graph type to its data and function


graph_data_mapping = {
    "Tradle": {"data_file": "data/all_countries.csv", "graph_function": show_country},
    "AGE 2022": {
        "data_file": ("data/country_data_palo.xlsx", 0),
        "graph_function": show_piramid,
    },
    "SURFACE 2019": {
        "data_file": ("data/country_data_palo.xlsx", 1),
        "graph_function": show_country_palo,
    },
    "DEATHS 2019": {
        "data_file": ("data/country_data_palo.xlsx", 2),
        "graph_function": show_country_palo,
    },
    "DEATHS BY AGE 2021": {
        "data_file": ("data/country_data_palo.xlsx", 3),
        "graph_function": show_bar_deaths,
    },
    "EMIGRANTES RESIDENTES 2020": {
        "data_file": ("data/country_data_palo.xlsx", 4),
        "graph_function": show_country_palo,
    },
}
if "data" not in st.session_state:
    data = {}
    for table, dicc in graph_data_mapping.items():
        if table == "Tradle":
            data[table] = pandas.read_csv(dicc["data_file"])

        else:
            data_file_path, sheet_number = dicc["data_file"]
            data[table] = pandas.read_excel(data_file_path, sheet_number)
            # if table == "SURFACE 2019":
            #     data["SURFACE 2019"] = data["SURFACE 2019"].drop(columns=["Total km^2"])
            data[table] = data[table].melt(id_vars="Country")
    st.session_state.data = data
data = st.session_state.data


#################################################
# INIT
#################################################
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "graficos" not in st.session_state:
    st.session_state.graficos = 0
puntos_graficos = {0: 0, 1: 1, 2: 2, 3: 4, 4: 6, 5: 8, 6: 8, 7: 8}
puntos = (
    20 - (st.session_state.intentos * 2) - puntos_graficos[st.session_state.graficos]
)

random.seed(current_date)
Country_name = random.choice(data["Tradle"].Country.unique())


#################################################
# Gráficos
#################################################
if "list_graph" not in st.session_state:
    st.session_state.list_graph = list(graph_data_mapping.keys())
    random.seed(current_date)
    random.shuffle(st.session_state.list_graph)

# Display the selected graph type on the screen
precio = (
    puntos_graficos[st.session_state.graficos + 1]
    - puntos_graficos[st.session_state.graficos]
)
if st.button(f"Generar otro gráfico", disabled=st.session_state.graficos >= 5):
    st.session_state.graficos += 1
    precio = (
        puntos_graficos[st.session_state.graficos + 1]
        - puntos_graficos[st.session_state.graficos]
    )


st.write(f"Precio de un nuevo grafico: {precio} puntos")


for i in range(min(st.session_state.graficos + 1, 6)):
    selected_graph_type = st.session_state.list_graph[i]

    # Load data and display the graph
    graph_function = graph_data_mapping[selected_graph_type]["graph_function"]

    df_Country = data[selected_graph_type][
        data[selected_graph_type].Country == Country_name
    ]
    if len(df_Country) == 0:
        st.write(
            f"No valid graphs of {selected_graph_type} found for this country, la vida es dura."
        )
    else:
        random_colors = get_random_colors(length=len(df_Country), seed=current_date)

        fig = (
            graph_function(df_Country)
            if selected_graph_type in ["Tradle","DEATHS BY AGE 2021","AGE 2022"]
            else graph_function(df_Country, selected_graph_type, random_colors)
        )

        st.plotly_chart(fig)


##############################################################
# Lista de eleccion
##################################################################


Country_namelist = list(data["Tradle"].Country.unique())
Country_namelist.sort()
# Agregar una opción vacía al principio de la lista
Country_namelist.insert(0, "")

# Crear el cuadro desplegable con la opción predeterminada vacía

selected_Country = st.selectbox("Selecciona un país:", Country_namelist, index=0, key="country_selector")



# Agregar un botón

if "text" not in st.session_state:
    st.session_state.text = ""


puntos = (
    20 - (st.session_state.intentos * 2) - puntos_graficos[st.session_state.graficos]
)
# Lógica para incrementar intentos cuando se presiona el botón
if st.button(
    "Enviar (Cada intento pierdes 2 puntos)",
    key="my_button",
    disabled=st.session_state.intentos >= 7,
):

    if st.session_state.intentos <= 7 and selected_Country != "" :
        if selected_Country == Country_name:
            # exito
            st.session_state.text = (
                st.session_state.text
                + f'{str(st.session_state.intentos)} - <font color="green"> {selected_Country} </font><br>'
            )
            st.session_state.text = (
                st.session_state.text + f"Has conseguido {puntos} puntos"
            )
        else:
            distance = countries_distances_df[Country_name][selected_Country]
            direction = DIRECTIONS_EMOJI[countries_direction_df[Country_name][selected_Country]]
            st.session_state.intentos += 1
            st.session_state.text = (
                st.session_state.text
                + f'{str(st.session_state.intentos)} - <font color="red"> {selected_Country} </font>- {distance} km {direction} <br>'
            )
            selected_Country = ""


            if st.session_state.intentos == 6:
                puntos = 0
                st.session_state.text = (
                    st.session_state.text
                    + f"Has conseguido 0 puntos, el pais era {Country_name}"
                )

    # Display the styled text
st.write(st.session_state.text, unsafe_allow_html=True)

if puntos:
    puntos = (
        20 - (st.session_state.intentos * 2) - puntos_graficos[st.session_state.graficos]
    )
estrellas= f"{puntos} - "
for _ in range (puntos):
    estrellas=estrellas+'⭐'
st.write(f" {estrellas} ")
