# %% [markdown]
# --- IMPORTACIONES ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

# %% [markdown]
# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(layout="wide")
eje_desigualdad = 'Eje de desigualdad 4'
years = [2017, 2022]
quintiles = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

st.title("🏥 Monitor de Desigualdades en Salud - Región Metropolitana")
st.warning("**Datos fake generados para prototipo**")
st.warning("Los resultados se presentan solo a nivel de quintil, ya que el tamaño muestral no permite desagregación comunal válida.")

# %% [markdown]
# --- SELECCIÓN DEL INDICADOR ---
indicador_salud = st.sidebar.selectbox(
    "📌 Selecciona el indicador de salud:",
    options=[
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
        "Tasa de lactancia materna exclusiva a los 6 meses de edad",
    ]
)

# %% [markdown]
# --- DATOS DE ENTRADA BASE ---
COMUNAS_RM = [
    'Alhué', 'Buin', 'Calera de Tango', 'Cerrillos', 'Cerro Navia', 'Colina', 'Conchalí',
    'Curacaví', 'El Bosque', 'El Monte', 'Estación Central', 'Huechuraba', 'Independencia',
    'Isla de Maipo', 'La Cisterna', 'La Florida', 'La Granja', 'La Pintana', 'La Reina', 'Lampa',
    'Las Condes', 'Lo Barnechea', 'Lo Espejo', 'Lo Prado', 'Macul', 'Maipú', 'Maria Pinto',
    'Melipilla', 'Ñuñoa', 'Padre Hurtado', 'Paine', 'Pedro Aguirre Cerda', 'Peñaflor',
    'Peñalolén', 'Pirque', 'Providencia', 'Pudahuel', 'Puente Alto', 'Quilicura', 'Quinta Normal',
    'Recoleta', 'Renca', 'San Bernardo', 'San Joaquín', 'San José de Maipo', 'San Miguel',
    'San Pedro', 'San Ramón', 'Santiago', 'Talagante', 'Tiltil', 'Vitacura'
]
comunas_aleatorias = random.sample(COMUNAS_RM, k=3 * len(quintiles))
quintil_dict = {
    q: comunas_aleatorias[i*3:(i+1)*3]
    for i, q in enumerate(quintiles)
}

# %% [markdown]
# --- GENERACIÓN DE TABLA BASE CON DATOS SIMULADOS ---
rows_base = []
for year in years:
    for q in quintiles:
        comuna_list = quintil_dict[q]
        poblacion_total = np.random.randint(300000, 1000000)
        casos = np.random.randint(150, 800)
        tasa = (casos / poblacion_total) * 100000
        ic_min = max(tasa - np.random.uniform(0.5, 2.0), 0)
        ic_max = tasa + np.random.uniform(0.5, 2.0)

        rows_base.append({
            'Año': year,
            'Quintil': q,
            'Comunas': ', '.join(comuna_list),
            'Grupo Desigualdad': indicador_salud,
            'N° Casos': casos,
            'Población Total': poblacion_total,
            'Tasa Incidencia (x100k)': round(tasa, 2),
            'IC 95%': f"{round(ic_min, 2)} - {round(ic_max, 2)}"
        })

tabla_base = pd.DataFrame(rows_base)

# %% [markdown]
# --- VISUALIZACIÓN DE LA TABLA BASE ---
st.write(f"## 📊 Tabla Base por Quintil - {eje_desigualdad} ({indicador_salud})")
st.dataframe(tabla_base, use_container_width=True)

# %% [markdown]
# --- Conceptos ---
st.markdown("""
### 📖 Conceptos
- **IRD (Índice Relativo de Desigualdad):**  
  Razón teórica entre el extremo más desfavorecido (0%) y más favorecido (100%) de la distribución poblacional **ordenada por el eje de desigualdad**. 
    - \>1: Desigualdad perjudica a grupos desfavorecidos  
    - <1: Desigualdad beneficia a grupos desfavorecidos  
  *- Calculado mediante regresión de Poisson sobre rangos poblacionales acumulados.*
- **IAD (Índice Absoluto de Desigualdad):**  
  Diferencia absoluta teórica en tasas entre extremos de la gradiente social, **ajustada por la distribución poblacional**. 
  - Representa la pendiente de la regresión (casos/100k hab. por unidad de rango).
  - Ejemplo: IAD=10 significa 10 casos adicionales por 100k hab. por cada 100% de desventaja acumulada.
- Una **brecha creciente** entre quintiles refleja empeoramiento de la equidad en salud, 
  pero debe confirmarse con IRD/IAD para considerar toda la distribución.
""")

# %% [markdown]
# --- CÁLCULO DE BRECHAS Y DESIGUALDAD ---
def calcular_resumen(df):
    resumen = []
    for year in years:
        df_year = df[df['Año'] == year]
        tasas = df_year.set_index('Quintil')['Tasa Incidencia (x100k)'].sort_index()
        tasa_q1 = tasas['Q1']
        tasa_q5 = tasas['Q5']
        brecha_abs = tasa_q5 - tasa_q1
        brecha_rel = tasa_q5 / tasa_q1 if tasa_q1 != 0 else np.nan
        rr_min = round(brecha_rel - np.random.uniform(0.1, 0.4), 2)
        rr_max = round(brecha_rel + np.random.uniform(0.1, 0.4), 2)
        irs = round(np.random.uniform(1.5, 3.0), 3)
        iads = round(np.random.uniform(8.0, 15.0), 3)

        resumen.append({
            'Año': year,
            'Tasa Q1': round(tasa_q1, 2),
            'Tasa Q5': round(tasa_q5, 2),
            'Brecha Absoluta': round(brecha_abs, 2),
            'Brecha Relativa': round(brecha_rel, 2),
            'RR (IC 95%)': f"{round(brecha_rel, 2)} ({rr_min} - {rr_max})",
            'IRD': irs,
            'IAD': iads,
        })
    return pd.DataFrame(resumen)

tabla_resumen = calcular_resumen(tabla_base)

# %% [markdown]
# --- VISUALIZACIÓN DEL RESUMEN DE DESIGUALDAD ---
st.subheader(f"📉 Resumen de Desigualdades por Año - {eje_desigualdad} ({indicador_salud})")
tabla_transpuesta = tabla_resumen.set_index('Año').T
def color_semaforo_transpuesta(val, col_name):
    try:
        # Convertir a float por si hay datos no numéricos
        num_val = float(val)
    except ValueError:
        return ''
    
    if col_name == 'Brecha Absoluta':
        # Usar valor absoluto para considerar ambos lados
        return 'background-color: #FFCDD2' if abs(num_val) > 10 else ''
    elif col_name == 'IRD':
        # Usar valor absoluto para considerar ambos lados
        return 'background-color: #C8E6C9' if abs(num_val) < 2 else ''
    return ''

styled = tabla_transpuesta.style
for variable in ['Brecha Absoluta', 'IRD']:
    # Aplicar solo si la fila existe en el DataFrame
    if variable in tabla_transpuesta.index:
        styled = styled.apply(
            lambda row, var=variable: [color_semaforo_transpuesta(v, var) for v in row],
            axis=1, 
            subset=pd.IndexSlice[variable, :]
        )

st.dataframe(styled, use_container_width=True)

st.markdown("""  
🟥 **Brecha Absoluta** destacada en rojo indica una diferencia mayor a 10 casos por 100,000 habitantes, lo que sugiere una alta desigualdad.<br>  
🟩 **IRD** en verde señala valores menores a 2, lo que indica una menor desigualdad relativa entre quintiles.  
""", unsafe_allow_html=True)
# %% [markdown]
# --- INTERPRETACIÓN DINÁMICA ---
st.write("### 📅 Selección de año para interpretar los resultados")
anio_seleccionado = st.selectbox("Selecciona el año a visualizar", options=years)
filtro = tabla_resumen[tabla_resumen['Año'] == anio_seleccionado]
tasa_q1_sel = filtro['Tasa Q1'].values[0]
tasa_q5_sel = filtro['Tasa Q5'].values[0]
brecha_abs_sel = filtro['Brecha Absoluta'].values[0]

st.markdown(f"""
### 🔍 Interpretación para el año {anio_seleccionado}

- En {anio_seleccionado}, la tasa en el quintil más desfavorecido (Q1) fue de {tasa_q1_sel} casos por 100,000, mientras que en el quintil más favorecido (Q5) fue de {tasa_q5_sel}.
- Esto representa una brecha absoluta de {brecha_abs_sel:.2f} casos por 100,000 habitantes.
- Una brecha creciente puede indicar un empeoramiento del indicador de salud según {indicador_salud}, según el eje de desigualdad estudiado ({eje_desigualdad}).
""")

# %% [markdown]
# --- GRÁFICO DE BARRAS CON TODOS LOS AÑOS ---
tabla_base[['IC Inferior', 'IC Superior']] = tabla_base['IC 95%'].str.split(' - ', expand=True).astype(float)

fig = go.Figure()
for year in years:
    df_year = tabla_base[tabla_base['Año'] == year]
    fig.add_trace(go.Bar(
        x=df_year['Quintil'],
        y=df_year['Tasa Incidencia (x100k)'],
        name=str(year),
        error_y=dict(
            type='data',
            symmetric=False,
            array=df_year['IC Superior'] - df_year['Tasa Incidencia (x100k)'],
            arrayminus=df_year['Tasa Incidencia (x100k)'] - df_year['IC Inferior']
        ),
        text=df_year['IC 95%'],
        hoverinfo='x+y+text'
    ))

fig.update_layout(
    barmode='group',
    title=f"Tasa Incidencia por Quintil y Año ({indicador_salud})",
    xaxis_title="Quintil",
    yaxis_title="Tasa Incidencia (x100k)",
    bargap=0.15,
    bargroupgap=0.1,
)

st.plotly_chart(fig, use_container_width=True)

# %% [markdown]
# --- GLOSARIO ---
st.sidebar.markdown("## 📚 Glosario")
st.sidebar.markdown("""
- **Tasa de Incidencia:** Casos nuevos por 100,000 habitantes.
- **Brecha Relativa:** Razón Q5 / Q1.
- **IRD:** Índice Relativo de Desigualdad.
- **IAD:** Índice Absoluto de Desigualdad.
- **Quintil:** 20% de la población según eje de desigualdad.
""")
