# -*- coding: utf-8 -*-
"""
Código Python del Algoritmo de Búsqueda Gravitacional (GSA) para soporte de decisiones agrícolas
Propósito: Definir la función de fitness para optimizar la selección de cultivos y estrategias de manejo
"""

import numpy
import pandas

# Variables globales para almacenar datos del terreno y cultivos
datos_terreno = None
datos_cultivos = None

def establecer_datos(terreno, cultivos):
    """Establecer los datos globales del terreno y cultivos"""
    global datos_terreno, datos_cultivos
    datos_terreno = terreno
    datos_cultivos = cultivos

def FitnessAgricola(x):
    """Función de fitness para optimización agrícola"""
    if datos_terreno is None or datos_cultivos is None:
        print("Error: Datos del terreno o cultivos no cargados")
        return 1e10
    
    # Estructura del agente: [id_cultivo, fecha_siembra, volúmenes_riego (10), desplazamiento_cosecha, dosis_fertilizante (10)]
    id_cultivo = int(round(x[0]))  # Forzar entero para el cultivo
    fecha_siembra = x[1]
    volumenes_riego = x[2:12]
    desplazamiento_cosecha = x[12]
    dosis_fertilizante = x[13:]
    
    # Validar id_cultivo
    if id_cultivo < 0 or id_cultivo >= len(datos_cultivos):
        print(f"Error: ID de cultivo inválido: {id_cultivo}")
        return 1e10
    
    cultivo = datos_cultivos.iloc[id_cultivo]
    duracion_crecimiento = cultivo['duracion_crecimiento']
    
    # Calcular fecha de cosecha
    fecha_cosecha = fecha_siembra + duracion_crecimiento + desplazamiento_cosecha
    
    # Validar fechas con tolerancia
    fecha_siembra = round(fecha_siembra)  # Redondear para consistencia
    fecha_cosecha = round(fecha_cosecha)
    if not (1 <= fecha_siembra <= 30):
        print(f"Parámetros inválidos: fecha_siembra={fecha_siembra} fuera de [1, 30]")
        return 1e10
    if not (1 <= fecha_cosecha <= 180):
        print(f"Parámetros inválidos: fecha_cosecha={fecha_cosecha} fuera de [1, 180]")
        return 1e10
    
    # Verificar datos de cosecha
    datos_cosecha = datos_terreno[datos_terreno['dia'] == fecha_cosecha]
    if datos_cosecha.empty:
        print(f"No hay datos para fecha_cosecha={fecha_cosecha}")
        return 1e10
    
    # Calcular rendimiento
    rendimiento_max = 1000  # kg/ha
    rendimiento_por_agua = 10  # kg/mm
    rendimiento_por_fertilizante = 20  # kg/kg
    total_agua = sum(volumenes_riego)
    total_fertilizante = sum(dosis_fertilizante)
    
    # Ajustar rendimiento según necesidades
    necesidad_agua = cultivo['necesidad_agua_vegetativa'] if (fecha_cosecha - fecha_siembra) / 2 > (datos_terreno['dia'].max() - fecha_siembra) else cultivo['necesidad_agua_floracion']
    necesidad_nutrientes = cultivo['necesidad_nutrientes']
    factor_rendimiento = min(1.0, total_agua / max(necesidad_agua, 1e-6), total_fertilizante / max(necesidad_nutrientes, 1e-6))
    rendimiento_kg = min(rendimiento_max, (rendimiento_por_agua * total_agua + rendimiento_por_fertilizante * total_fertilizante) * factor_rendimiento)
    
    # Obtener precio de mercado
    precio_mercado = cultivo['precio_mercado']
    
    # Calcular costos
    dias_validos = datos_terreno[datos_terreno['dia'].isin(range(int(fecha_siembra), int(fecha_cosecha) + 1))]
    if dias_validos.empty:
        print(f"No hay datos para días {int(fecha_siembra)} a {int(fecha_cosecha)}")
        return 1e10
    
    costo_agua = cultivo['costo_agua'] * cultivo['dificultad_cultivo']
    costo_fertilizante = cultivo['costo_fertilizante'] * cultivo['dificultad_cultivo']
    costo_total = sum(costo_agua * vol for vol in volumenes_riego) + sum(costo_fertilizante * dosis for dosis in dosis_fertilizante)
    
    # Ganancia neta
    ingresos = rendimiento_kg * precio_mercado
    ganancia = ingresos - costo_total
    
    # Penalizar prácticas insostenibles
    for i, dia in enumerate(range(int(fecha_siembra), int(fecha_cosecha), 10)):
        if i >= len(volumenes_riego):
            break
        datos_dia = datos_terreno[datos_terreno['dia'] == dia]
        if datos_dia.empty:
            print(f"No hay datos para dia={dia}")
            continue
        humedad_suelo = datos_dia['humedad_suelo'].iloc[0] + volumenes_riego[i] - datos_dia['promedio_precipitaciones'].iloc[0]
        if humedad_suelo > 80 or humedad_suelo < 20:
            ganancia -= 1000
    
    if numpy.isnan(ganancia):
        print("Cálculo de ganancia resultó en NaN")
        return 1e10
    
    return -ganancia

def obtener_detalles_funcion(a):
    # [nombre, lb, ub, dim]
    param = {
        0: ["FitnessAgricola", [0, 1] + [0]*10 + [-10] + [0]*10, [2, 30] + [50]*10 + [10] + [20]*10, 23]
    }
    return param.get(a, "nada")