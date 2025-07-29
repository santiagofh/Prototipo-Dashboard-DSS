import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# --- Configuración general ---
grupo_indicador = 'TBC'
st.title("🏥 Monitor de Desigualdades en Salud - Región Metropolitana")
st.warning("**Datos fake generados para prototipo**")
st.warning("Los resultados se presentan solo a nivel de quintil, ya que el tamaño muestral no permite desagregación comunal válida.")

# --- Selección eje de desigualdad ---
grupo_desigualdad = st.sidebar.selectbox(
    "📌 Selecciona el eje de desigualdad:",
    options=["Pobreza por ingresos", "Escolaridad", "Migración", "Hacinamiento"]
)

# --- Variables base ---
quintiles = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
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

# Asignar comunas aleatorias a quintiles
comunas_aleatorias = random.sample(COMUNAS_RM, k=3 * len(quintiles))
quintil_dict = {
    q: comunas_aleatorias[i*3:(i+1)*3]
    for i, q in enumerate(quintiles)
}

years = [2017, 2022]
comunas_por_quintil = 3

# --- Crear tabla base con datos simulados ---
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
            'Grupo Desigualdad': grupo_desigualdad,
            'N° Casos': casos,
            'Población Total': poblacion_total,
            'Tasa Incidencia (x100k)': round(tasa, 2),
            'IC 95%': f"{round(ic_min, 2)} - {round(ic_max, 2)}"
        })

tabla_base = pd.DataFrame(rows_base)

# --- Selección dinámica año para visualizar tabla y texto ---
st.sidebar.markdown("### 📅 Selección de año")
anio_seleccionado = st.sidebar.selectbox("Selecciona el año a visualizar", options=years)

# --- Mostrar tabla base filtrada por año seleccionado ---
st.write(f"## 📊 Tabla Base por Quintil - {grupo_indicador} ({grupo_desigualdad}) - Año {anio_seleccionado}")
tabla_filtrada = tabla_base[tabla_base['Año'] == anio_seleccionado]
st.dataframe(tabla_filtrada, use_container_width=True)

# --- Interpretación breve ---
st.markdown("""
### 📖 Interpretación rápida
- Una **brecha creciente** entre quintiles indica un aumento en la desigualdad, lo que suele ser negativo para la equidad en salud.
- Una **IRD (Índice Relativo de Desigualdad)** mayor que 1 indica desigualdad creciente; por ejemplo, IRD = 2.1 significa que la tasa en el grupo más favorecido es 2.1 veces la del más desfavorecido.
- Una **IAD (Índice Absoluto de Desigualdad)** mide la diferencia absoluta en tasas, por ejemplo, IAD = 12.3 indica 12.3 casos adicionales por 100,000 personas entre extremos.
- Importa la desigualdad en cada eje porque refleja distintas barreras sociales que afectan la salud.
""")

# --- Función para calcular resumen de desigualdad por año ---
def calcular_resumen(df):
    resumen = []
    for year in years:
        df_year = df[df['Año'] == year].copy()
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

# --- Mostrar resumen de desigualdades ---
st.subheader(f"📉 Resumen de Desigualdades por Año - {grupo_indicador} ({grupo_desigualdad})")
def color_semaforo(row):
    color_abs = 'background-color: #FFCDD2' if row['Brecha Absoluta'] > 10 else ''
    color_ird = 'background-color: #C8E6C9' if row['IRD'] < 2 else ''
    return [color_abs if col == 'Brecha Absoluta' else color_ird if col == 'IRD' else '' for col in row.index]
st.dataframe(tabla_resumen.style.apply(color_semaforo, axis=1), use_container_width=True)

# --- Texto interpretativo dinámico para el año seleccionado ---
tasa_q1_sel = tabla_resumen.loc[tabla_resumen['Año'] == anio_seleccionado, 'Tasa Q1'].values[0]
tasa_q5_sel = tabla_resumen.loc[tabla_resumen['Año'] == anio_seleccionado, 'Tasa Q5'].values[0]
brecha_abs_sel = tabla_resumen.loc[tabla_resumen['Año'] == anio_seleccionado, 'Brecha Absoluta'].values[0]

st.markdown(f"""
### 🔍 Interpretación para el año {anio_seleccionado}

- En {anio_seleccionado}, la tasa en el quintil más desfavorecido (Q1) fue de {tasa_q1_sel} casos por 100,000, mientras que en el quintil más favorecido (Q5) fue de {tasa_q5_sel}.
- Esto representa una brecha absoluta de {brecha_abs_sel:.2f} casos por 100,000 habitantes.
- Una brecha creciente puede indicar un empeoramiento de la desigualdad en salud según el eje de {grupo_desigualdad}.
""")

# --- Gráfico de barras CON TODOS LOS AÑOS ---
# Preparamos datos para barras con todos los años, agrupando por Año y Quintil
tabla_base[['IC Inferior', 'IC Superior']] = tabla_base['IC 95%'].str.split(' - ', expand=True).astype(float)

fig_bar = px.bar(
    tabla_base,
    x='Quintil',
    y='Tasa Incidencia (x100k)',
    color='Año',
    barmode='group',
    error_y=tabla_base['IC Superior'] - tabla_base['Tasa Incidencia (x100k)'],
    error_y_minus=tabla_base['Tasa Incidencia (x100k)'] - tabla_base['IC Inferior'],
    hover_data=['Comunas', 'N° Casos', 'Población Total', 'IC 95%'],
    title=f"Tasa Incidencia por Quintil y Año ({grupo_desigualdad})"
)
fig_bar.update_layout(xaxis_title="Quintil", yaxis_title="Tasa Incidencia (x100k)")
# st.plotly_chart(fig_bar, use_container_width=True)

# --- Gráfico de líneas con evolución temporal de brechas ---
import plotly.graph_objects as go

# Preparar datos por quintil y año
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
    title=f"Tasa Incidencia por Quintil y Año ({grupo_desigualdad})",
    xaxis_title="Quintil",
    yaxis_title="Tasa Incidencia (x100k)",
    bargap=0.15,
    bargroupgap=0.1,
)

st.plotly_chart(fig, use_container_width=True)

# --- Glosario ---
st.sidebar.markdown("## 📚 Glosario")
st.sidebar.markdown("""
- **Tasa de Incidencia:** número de casos nuevos por cada 100,000 habitantes.
- **Brecha Relativa:** razón entre la tasa del quintil más favorecido y la del más desfavorecido.
- **IRD (Índice Relativo de Desigualdad):** mide la desigualdad relativa en la población; IRD > 1 indica desigualdad.
- **IAD (Índice Absoluto de Desigualdad):** diferencia absoluta entre las tasas de los extremos.
- **Quintil:** grupo que divide a la población en cinco partes iguales según el eje de desigualdad.
""")
