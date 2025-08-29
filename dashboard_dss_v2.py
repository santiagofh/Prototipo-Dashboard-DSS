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
        # 🏥 Dashboard de Determinantes Sociales de Salud (DSS)
        """
    )

    st.image(
        "https://www.paho.org/sites/default/files/styles/top_hero/public/2025-04/banner-dss2.jpg?h=5a93717a&itok=ycLYggyw",
        use_container_width =True
    )
    st.caption("(Imagen original de la web de la OPS)[https://www.paho.org/es/temas/determinantes-sociales-salud]")
    st.write(
        """
        ## 📊 Monitoreo de inequidades en salud y determinantes sociales en la Región Metropolitana
        """
    )
        
    # ✨ Texto de introducción
    st.markdown(
        """
        Este dashboard es parte de la cooperación técnica entre **OPS/OMS** y la **SEREMI de Salud de la Región Metropolitana**, 
        en el marco de la *Iniciativa Especial para la Acción sobre los Determinantes Sociales de la Equidad en Salud*.
        """,
        unsafe_allow_html=True
    )

    # 💡 Pregunta motivadora
    st.info(
        "🌍 **La salud no depende solo de decisiones individuales: también depende de dónde y cómo vivimos.**\n\n"
        "Este visor te invita a explorar cómo los determinantes sociales influyen en la salud de las personas "
        "en la Región Metropolitana, y qué desigualdades persisten entre comunas."
    )

    st.markdown("---")

    # 🔎 Cita inspirada en la OMS
    st.markdown(
        """
        > *"Los determinantes sociales de la salud son las circunstancias en que las personas nacen, crecen, 
        trabajan, viven y envejecen, y las fuerzas más amplias que conforman las condiciones de la vida cotidiana."*  
        **— [Organización Mundial de la Salud](https://www.who.int/es/news-room/fact-sheets/detail/social-determinants-of-health?utm_source=chatgpt.com)**
        """
    )
    with st.expander("📚 ¿Quieres aprender más sobre estos conceptos?"):
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

    # 📊 Explicación técnica
    st.markdown(
        """
        El visor utiliza **datos comunales** para analizar brechas en salud asociadas a **ejes de inequidad**.  
        Se aplican métricas como:  
        - Tasas de incidencia ponderadas  
        - Brechas absolutas y relativas  
        - Índices de desigualdad 📈  
        """
    )

    with st.expander("📊 Aprende más sobre estas métricas"):
        st.markdown(
            """
            🔹 **Tasa de incidencia ponderada:**  
            Es el número de casos nuevos de una enfermedad por cada 100,000 habitantes, ajustado para que la comparación entre quintiles o comunas sea justa considerando el tamaño de la población de cada grupo.

            🔹 **Brecha absoluta:**  
            Diferencia directa entre los valores de un indicador entre los grupos más desfavorecidos y los más favorecidos. Por ejemplo, si la tasa de tuberculosis es 50 en Q1 y 20 en Q5, la brecha absoluta es 30.

            🔹 **Brecha relativa:**  
            Razón entre los valores de los extremos. Siguiendo el ejemplo anterior: 50/20 = 2.5. Indica cuántas veces es más alta la tasa en el grupo más vulnerable respecto al más favorecido.

            🔹 **Índices de desigualdad (IRD/IAD) 📈:**  
            - **IRD (Índice Relativo de Desigualdad):** Resume la desigualdad relativa a lo largo de toda la distribución, no solo extremos. >1 indica que los desfavorecidos tienen peores resultados.  
            - **IAD (Índice Absoluto de Desigualdad):** Resume la desigualdad absoluta a lo largo de la distribución. Representa cuántos casos adicionales hay por cada 100,000 habitantes al comparar extremos acumulados.

            Estos indicadores permiten ver no solo diferencias puntuales, sino cómo se distribuye la salud a lo largo de toda la población.
            """
        )



    st.markdown("---")
    st.write("## 🔎 Ejes de desigualdad e Indicadores a explorar")
    st.info(
        "❓ **¿Qué desigualdades en salud vamos a explorar en este dashboard?**\n\n"
        "Primero, abre la página del **eje de desigualdad** que te interese, "
        "y luego selecciona un **Indicador de salud** para ver cómo varía entre quintiles."
    )

    # 🧩 Ejes de desigualdad en columnas
    st.write("### Ejes de desigualdad")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- 💰 **Pobreza por ingreso**")
        st.markdown("- 🌍 **Migración**")
    with col2:
        st.markdown("- 🎓 **Escolaridad**")
        st.markdown("- 🏠 **Hacinamiento**")

    # 📌 Indicadores con bullets destacados
    st.write("### 📌 Indicadores priorizados")

    indicadores = [
        "Tasa de incidencia de Tuberculosis",
        "Tasa de incidencia de VIH y/o Sífilis",
        "Prevalencia de caries dentales en menores de 6 años",
        "Cobertura efectiva de control de Diabetes Mellitus tipo II",
        "Tasa de mortalidad infantil",
        "Tasa de mortalidad por enfermedades cardiovasculares",
        "Tasa de mortalidad por suicidio",
        "Tasa de mortalidad por Cáncer Cervicouterino",
        "Cobertura de detección precoz de Cáncer de Mama mediante mamografías",
        "Cobertura de examen de medicina preventiva del adulto (EMPA)",
        "Porcentaje de recién nacidos con bajo peso al nacer (< 2.500 g)",
        "Tasa de lactancia materna exclusiva a los 6 meses de edad"
    ]

    # Dividir en dos columnas
    col1, col2 = st.columns(2)

    # Primera mitad en col1, segunda mitad en col2
    for i, ind in enumerate(indicadores, 1):
        if i <= len(indicadores) // 2:
            col1.markdown(f"{i}. {ind}")
        else:
            col2.markdown(f"{i}. {ind}")

#%%
HORIZONTAL = "IMG/GEOSITAS_inf_mapas - copia.png"
ICON = "IMG/Logo_GeoSitas(15%) (Icono Siigsa 64x64).png"
st.logo(HORIZONTAL, icon_image=ICON)
# %%
pages = {
    "Menu principal": [
        st.Page(home, default=True, title="Pagina de inicio - DSS", icon=":material/home:")
    ],
    "Ejes de desigualdad": [
        st.Page('dss_eje_1.py', title="Pobreza de ingresos", icon=":material/public:"),
        st.Page('dss_eje_2.py', title="Migración", icon=":material/public:"),
        st.Page('dss_eje_3.py', title="Escolaridad", icon=":material/public:"),
        st.Page('dss_eje_4.py', title="Hacinamiento", icon=":material/public:"),
    ]
}
pg = st.navigation(pages)
pg.run()
