#%%
# Importar librerias
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import poisson
# Indicadores de desigualdad de TBC
#%% 
# Calculo de quintiles por pobreza
pobreza_22=pd.read_excel(r"DATA/INDICADORES COMUNALES CASEN 2022 RMS.xlsx", sheet_name=" POBREZA DE INGRESOS (SAE)", skiprows=4)
pobreza_22=pobreza_22.iloc[:52]
pobreza_22=pobreza_22[['Comuna','No pobres']]
# Crear variable categórica de quintiles
pobreza_22['Quintil_Pobreza'] = pd.qcut(
    pobreza_22['No pobres'], 
    q=5, 
    labels=['Q1 (más desaventajado)','Q2','Q3','Q4','Q5 (más aventajado)']
)

# Verificar distribución
print("Comunas por quintil:")
print(pobreza_22['Quintil_Pobreza'].value_counts().sort_index())
# Guardar resultados
# %%
tb_22=pd.read_excel(r"DATA/DSS_TASAS_TB.xlsx")
tb_22=tb_22.loc[tb_22.Año==2022]
tb_22
# %%
tb_pobreza_22=tb_22.merge(pobreza_22,on="Comuna", how='left')

# %%
# Cargar datos

agg_data = tb_pobreza_22.groupby('Quintil_Pobreza').agg(
    Total_Casos=('Casos_TB', 'sum'),
    Total_Poblacion=('Poblacion', 'sum')
).reset_index()

agg_data['Tasa_Ponderada'] = (agg_data['Total_Casos'] / agg_data['Total_Poblacion']) * 100000

#%%

def calcular_ic_poisson(casos, poblacion, escala=100000, alpha=0.05):
    """
    Calcula IC exacto para tasas usando distribución Poisson
    casos: número total de casos observados
    poblacion: población total en el grupo
    escala: factor de escala para la tasa (default 100,000)
    alpha: nivel de significancia (default 0.05)
    """
    if casos == 0:
        li = 0
        ls = stats.chi2.ppf(1 - alpha/2, 2*(casos+1)) / 2 / poblacion * escala
    else:
        li = stats.chi2.ppf(alpha/2, 2*casos) / 2 / poblacion * escala
        ls = stats.chi2.ppf(1 - alpha/2, 2*(casos+1)) / 2 / poblacion * escala
    return li, ls

# Calcular tasas e IC para cada quintil
results = []
for quintil in sorted(agg_data['Quintil_Pobreza'].unique()):
    grupo = agg_data[agg_data['Quintil_Pobreza'] == quintil].iloc[0]
    casos = grupo['Total_Casos']
    poblacion = grupo['Total_Poblacion']
    tasa = grupo['Tasa_Ponderada']
    
    li, ls = calcular_ic_poisson(casos, poblacion)
    
    results.append({
        'Quintil': quintil,
        'Casos': casos,
        'Población': f"{poblacion:,.0f}",
        'Tasa (x100,000)': f"{tasa:.2f}",
        'IC 95%': f"({li:.2f} - {ls:.2f})",
        'Tasa_num': tasa,  # Para análisis posterior
        'IC_lower': li,    # Para gráficos
        'IC_upper': ls
    })

# Convertir a DataFrame
resultados_df = pd.DataFrame(results)
# %%
# Obtener datos de quintiles extremos
q1 = resultados_df[resultados_df['Quintil'] == 'Q1 (más desaventajado)'].iloc[0]
q5 = resultados_df[resultados_df['Quintil'] == 'Q5 (más aventajado)'].iloc[0]

# Brecha absoluta
brecha_abs = q1['Tasa_num'] - q5['Tasa_num']
brecha_abs_li = q1['IC_lower'] - q5['IC_upper']  # Límite conservador
brecha_abs_ls = q1['IC_upper'] - q5['IC_lower']  # Límite conservador

# Brecha relativa (Razón de Tasas)
rr = q1['Tasa_num'] / q5['Tasa_num']
log_rr = np.log(rr)
se_log_rr = np.sqrt(1/q1['Casos'] + 1/q5['Casos'])
rr_li = np.exp(log_rr - 1.96 * se_log_rr)
rr_ls = np.exp(log_rr + 1.96 * se_log_rr)

# Agregar fila de brechas
# Crear DataFrames para las nuevas filas
brecha_df = pd.DataFrame({
    'Quintil': ['Brecha Q1 vs Q5'],
    'Casos': [''],
    'Población': [''],
    'Tasa (x100,000)': [f"{brecha_abs:.2f}"],
    'IC 95%': [f"({brecha_abs_li:.2f} - {brecha_abs_ls:.2f})"],
    'Tasa_num': [brecha_abs],
    'IC_lower': [brecha_abs_li],
    'IC_upper': [brecha_abs_ls]
})

rr_df = pd.DataFrame({
    'Quintil': ['Razón Q1/Q5'],
    'Casos': [''],
    'Población': [''],
    'Tasa (x100,000)': [f"{rr:.2f}"],
    'IC 95%': [f"({rr_li:.2f} - {rr_ls:.2f})"],
    'Tasa_num': [rr],
    'IC_lower': [rr_li],
    'IC_upper': [rr_ls]
})

# Concatenar al DataFrame principal
resultados_df = pd.concat([
    resultados_df, 
    brecha_df,
    rr_df
], ignore_index=True)
# %%
# Calcular tasas e IC para cada quintil
results = []
for quintil in sorted(agg_data['Quintil_Pobreza'].unique()):
    grupo = agg_data[agg_data['Quintil_Pobreza'] == quintil].iloc[0]
    casos = grupo['Total_Casos']
    poblacion = grupo['Total_Poblacion']
    tasa = grupo['Tasa_Ponderada']
    
    li, ls = calcular_ic_poisson(casos, poblacion)
    
    results.append({
        'Quintil': quintil,
        'Casos': casos,
        'Población': f"{poblacion:,.0f}",
        'Tasa (x100,000)': f"{tasa:.2f}",
        'IC 95%': f"({li:.2f} - {ls:.2f})",
        'Tasa_num': tasa,  # Para análisis posterior
        'IC_lower': li,    # Para gráficos
        'IC_upper': ls
    })

# Convertir a DataFrame
resultados_df = pd.DataFrame(results)

# Obtener datos de quintiles extremos (Q1 y Q5)
q1 = resultados_df[resultados_df['Quintil'] == 'Q1 (más desaventajado)'].iloc[0]
q5 = resultados_df[resultados_df['Quintil'] == 'Q5 (más aventajado)'].iloc[0]

# Brecha absoluta
brecha_abs = q1['Tasa_num'] - q5['Tasa_num']
brecha_abs_li = q1['IC_lower'] - q5['IC_upper']  # Límite conservador
brecha_abs_ls = q1['IC_upper'] - q5['IC_lower']  # Límite conservador

# Brecha relativa (Razón de Tasas)
rr = q1['Tasa_num'] / q5['Tasa_num']
log_rr = np.log(rr)
se_log_rr = np.sqrt(1/q1['Casos'] + 1/q5['Casos'])
rr_li = np.exp(log_rr - 1.96 * se_log_rr)
rr_ls = np.exp(log_rr + 1.96 * se_log_rr)

# Crear DataFrames para las nuevas filas
brecha_df = pd.DataFrame({
    'Quintil': ['Brecha Q1 vs Q5'],
    'Casos': [''],
    'Población': [''],
    'Tasa (x100,000)': [f"{brecha_abs:.2f}"],
    'IC 95%': [f"({brecha_abs_li:.2f} - {brecha_abs_ls:.2f})"],
    'Tasa_num': [brecha_abs],
    'IC_lower': [brecha_abs_li],
    'IC_upper': [brecha_abs_ls]
})

rr_df = pd.DataFrame({
    'Quintil': ['Razón Q1/Q5'],
    'Casos': [''],
    'Población': [''],
    'Tasa (x100,000)': [f"{rr:.2f}"],
    'IC 95%': [f"({rr_li:.2f} - {rr_ls:.2f})"],
    'Tasa_num': [rr],
    'IC_lower': [rr_li],
    'IC_upper': [rr_ls]
})

# Concatenar al DataFrame principal
resultados_df = pd.concat([
    resultados_df, 
    brecha_df,
    rr_df
], ignore_index=True)

# Seleccionar y ordenar columnas para presentación
tabla_final = resultados_df[[
    'Quintil', 'Casos', 'Población', 
    'Tasa (x100,000)', 'IC 95%'
]]

# Formatear números grandes
tabla_final['Población'] = tabla_final['Población'].apply(
    lambda x: f"{int(x.replace(',', '')):,}" if isinstance(x, str) and x != '' else x
)

# Agregar encabezados descriptivos
tabla_final.columns = [
    'Grupo según nivel de pobreza', 
    'N° total de casos', 
    'Población total', 
    'Tasa de incidencia (por 100,000 hab)', 
    'Intervalo de Confianza 95%'
]

# Mostrar tabla
print("\n" + "="*80)
print("Análisis de Inequidades en Tuberculosis por Nivel de Pobreza")
print("Región Metropolitana, 2022")
print("="*80)
print(tabla_final.to_string(index=False))
print("\nNota: Quintiles construidos según % de pobreza por ingresos (Q1 = más pobre)")
# %%
