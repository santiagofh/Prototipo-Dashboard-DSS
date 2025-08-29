# %%
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# %%
def home():
    # 🎨 Encabezado con estilo
    st.image('IMG/seremi-100-años.png', width=300)
    st.write(
        """
        # Dashboard de Determinantes Sociales de Salud (DSS)
        """
    )

    st.image(
        "https://www.paho.org/sites/default/files/styles/top_hero/public/2025-04/banner-dss2.jpg?h=5a93717a&itok=ycLYggyw",
        use_container_width =True
    )
    st.caption("""
               [Imagen original de la web de la OPS](https://www.paho.org/es/temas/determinantes-sociales-salud)
               """)
    st.write(
        """
        ## Monitoreo de determinantes sociales en la Región Metropolitana
        """
    )
        

    # 🔎 Cita inspirada en la OMS
    st.markdown(
        """
        *"Los determinantes sociales de la salud son las circunstancias en que las personas nacen, crecen, 
        trabajan, viven y envejecen, y las fuerzas más amplias que conforman las condiciones de la vida cotidiana."*  
        **— [Organización Mundial de la Salud](https://www.who.int/es/news-room/fact-sheets/detail/social-determinants-of-health)**
        """
    )
    with st.expander("¿Quieres aprender más sobre estos conceptos?"):
        st.markdown(
            """
            Aquí encontrarás recursos confiables para profundizar:  

            🔹 **OPS/OMS - Determinantes Sociales de la Salud**  
            [Enlace oficial](https://www.paho.org/es/temas/determinantes-sociales-salud)  

            🔹 **OPS - Determinantes Sociales Ambientales Para Equidad en Salud**  
            [Enlace oficial](https://www.paho.org/es/determinantes-sociales-ambientales-para-equidad-salud)  

            Estos materiales pueden ayudarte a entender mejor los indicadores y las métricas de desigualdad que se presentan en el dashboard.
            """
        )
    st.markdown("---")
    st.write("## Indicadores de salud")
    # Diccionario: clave = texto del botón, valor = archivo dentro de pages/
    indicadores = {
        "Tasa de incidencia de Tuberculosis": "ind_01.py",
        "Tasa de incidencia de VIH y/o Sífilis": "ind_02.py",
        "Prevalencia de caries dentales en menores de 6 años": "ind_03.py",
        "Cobertura efectiva de control de Diabetes Mellitus tipo II": "ind_04.py",
    }

    # Crear botones en filas de 3
    for i in range(0, len(indicadores), 3):
        cols = st.columns(3)
        for col, (nombre, archivo) in zip(cols, list(indicadores.items())[i:i+3]):
            if col.button(nombre, use_container_width=True):
                st.switch_page(f"pages/{archivo}")  # Ruta relativa dentro de pages/
    st.image("IMG/Banner Linkedin Profesional Corporativo Gris.png")
    st.markdown("---")
    st.write("## Determinantes Sociales de Salud")

    # Diccionario: clave = texto del botón, valor = archivo dentro de pages/
    indicadores = {
        "Ingreso y pobreza": "dss_01.py",
        "Educación": "dss_02.py",
        "Trabajo y empleo": "dss_03.py",
        "Vivienda y entorno": "dss_04.py",
    }

    # Crear botones en filas de 3
    for i in range(0, len(indicadores), 3):
        cols = st.columns(3)
        for col, (nombre, archivo) in zip(cols, list(indicadores.items())[i:i+3]):
            if col.button(nombre, use_container_width=True):
                st.switch_page(f"pages/{archivo}")  # Ruta relativa dentro de pages/
    st.image("IMG/Banner Linkedin Profesional Corporativo Gris.png")

    st.markdown("---")
    st.write("## Eje de desigualdad")

    # Diccionario: clave = texto del botón, valor = archivo dentro de pages/
    indicadores = {
        "Desigualdad por género": "eje_01.py",
        "Desigualdad territorial": "eje_02.py",
        "Desigualdad por edad": "eje_03.py",
        "Desigualdad étnica": "eje_04.py",
    }

    # Crear botones en filas de 3
    for i in range(0, len(indicadores), 3):
        cols = st.columns(3)
        for col, (nombre, archivo) in zip(cols, list(indicadores.items())[i:i+3]):
            if col.button(nombre, use_container_width=True):
                st.switch_page(f"pages/{archivo}")  # Ruta relativa dentro de pages/
    st.image("IMG/Banner Linkedin Profesional Corporativo Gris.png")

#%%
HORIZONTAL = "IMG/GEOSITAS_inf_mapas - copia.png"
ICON = "IMG/Logo_GeoSitas(15%) (Icono Siigsa 64x64).png"
st.logo(HORIZONTAL, icon_image=ICON)
# %%
pages = {
    "Menu principal": [
        st.Page(home, default=True, title="Página de inicio - DSS", icon=":material/home:")
    ],
    "Indicadores de Salud": [
        st.Page('pages/ind_01.py', title="Tasa de incidencia de Tuberculosis", icon=":material/monitor_heart:"),
        st.Page('pages/ind_02.py', title="Tasa de incidencia de VIH y/o Sífilis", icon=":material/medication:"),
        st.Page('pages/ind_03.py', title="Prevalencia de caries en menores de 6 años", icon=":material/medical_services:"),
        st.Page('pages/ind_04.py', title="Cobertura control Diabetes Mellitus II", icon=":material/syringe:"),
    ],
    "Determinantes Sociales de Salud": [
        st.Page('pages/dss_01.py', title="Ingreso y pobreza", icon=":material/payments:"),
        st.Page('pages/dss_02.py', title="Educación", icon=":material/school:"),
        st.Page('pages/dss_03.py', title="Trabajo y empleo", icon=":material/work:"),
        st.Page('pages/dss_04.py', title="Vivienda y entorno", icon=":material/home_work:"),
    ],
    "Eje de desigualdad": [
        st.Page('pages/eje_01.py', title="Desigualdad por género", icon=":material/wc:"),
        st.Page('pages/eje_02.py', title="Desigualdad territorial", icon=":material/map:"),
        st.Page('pages/eje_03.py', title="Desigualdad por edad", icon=":material/calendar_month:"),
        st.Page('pages/eje_04.py', title="Desigualdad étnica", icon=":material/diversity_3:"),
    ]
}
pg = st.navigation(pages)
pg.run()

