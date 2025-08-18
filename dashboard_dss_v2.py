# %%
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# from streamlit_faker import get_streamlit_faker
#%%
def home():
    st.title('🏥 Dashboard de Determinantes Sociales de Salud (DSS)')

    # Subtítulo
    st.subheader('📊 Monitoreo de inequidades en salud y determinantes sociales en la Región Metropolitana')

    # Descripción
    st.write("""
    Este dashboard es parte de la cooperación técnica entre OPS/OMS y la SEREMI de Salud de la Región Metropolitana, 
    en el marco de la *Iniciativa Especial para la Acción sobre los Determinantes Sociales de la Equidad en Salud*.
    
    Su objetivo es apoyar la vigilancia y monitoreo de inequidades en salud, analizando cómo factores estructurales 
    y sociales se relacionan con la distribución de enfermedades y condiciones sanitarias en la región.
    """)

    st.write("""
    El visor utiliza datos comunales para analizar brechas en salud asociadas a ejes de inequidad. Se aplican métricas como tasas de incidencia ponderadas, brechas absolutas y relativas, 
    e índices de desigualdad 📈 para facilitar la interpretación de los datos.
    """)

    st.write("""
    🔎 En este visor a partir de los ejes de desigualdad:
    1. Pobreza por ingreso 
    2. Migración
    3. Escolaridad
    4. Hacinamiento
             
    Se analizan 12 indicadores clave de salud, priorizados por la SEREMI de Salud RM:

    1. **Tasa de incidencia de Tuberculosis**  
    2. **Tasa de incidencia de VIH y/o Sífilis**  
    3. **Prevalencia de caries dentales en menores de 6 años**  
    4. **Cobertura efectiva de control de Diabetes Mellitus tipo II**  
    5. **Tasa de mortalidad infantil**  
    6. **Tasa de mortalidad por enfermedades cardiovasculares**  
    7. **Tasa de mortalidad por suicidio**  
    8. **Tasa de mortalidad por Cáncer Cervicouterino**  
    9. **Cobertura de detección precoz de Cáncer de Mama mediante mamografías**  
    10. **Cobertura de examen de medicina preventiva del adulto (EMPA)**  
    11. **Porcentaje de recién nacidos con bajo peso al nacer (< 2.500 g)**  
    12. **Tasa de lactancia materna exclusiva a los 6 meses de edad**
    """)

#%%

#%%
pages = {
"Menu principal":[
    st.Page(home, default=True, title="Pagina de inicio - DSS", icon=":material/home:")
],
"Ejes de desigualdad" : [
    st.Page('dss_eje_1.py', title="Pobreza de ingresos", icon=":material/public:"),
    st.Page('dss_eje_2.py', title="Eje de desigualdad 2", icon=":material/public:"),
    st.Page('dss_eje_3.py', title="Eje de desigualdad 3", icon=":material/public:"),
    st.Page('dss_eje_4.py', title="Eje de desigualdad 4", icon=":material/public:"),
]
}
pg = st.navigation(pages)
pg.run()