import pandas as pd
import numpy as np

# Generar datos del terreno para 180 días
dias = range(1, 181)
datos_terreno = {
    'dia': dias,
    'temperatura': np.random.uniform(20, 30, 180),
    'promedio_precipitaciones': np.random.uniform(0, 10, 180),
    'humedad_suelo': np.random.uniform(20, 60, 180)
}
df_terreno = pd.DataFrame(datos_terreno)
df_terreno.to_csv('datos_terreno.csv', index=False)

# Generar datos de cultivos
datos_cultivos = {
    'cultivo': ['maiz', 'trigo', 'soya'],
    'duracion_crecimiento': [120, 130, 110],
    'necesidad_agua_vegetativa': [50.0, 45.0, 40.0],
    'necesidad_agua_floracion': [60.0, 55.0, 50.0],
    'necesidad_nutrientes': [30.0, 25.0, 35.0],
    'dificultad_cultivo': [1.2, 1.5, 1.3],
    'precio_mercado': [2.5, 2.0, 2.8],
    'costo_agua': [0.1, 0.1, 0.1],
    'costo_fertilizante': [0.2, 0.2, 0.2]
}
df_cultivos = pd.DataFrame(datos_cultivos)
df_cultivos.to_csv('datos_cultivos.csv', index=False)

print("CSVs generados: datos_terreno.csv, datos_cultivos.csv")