# -*- coding: utf-8 -*-
"""
Código Python del Algoritmo de Búsqueda Gravitacional (GSA) para soporte de decisiones agrícolas
Propósito: Módulo para ejecutar GSA y optimizar estrategias de manejo agrícola
"""

import GSA as gsa
import benchmarks as fr
import numpy
import pandas
import time
import matplotlib.pyplot as plt
import io
import base64
import os

def run_gsa(terreno_data, cultivos_data, tamano_poblacion=50, iteraciones=200):
    """
    Ejecuta el GSA con los datos proporcionados y parámetros.
    Retorna un diccionario con los resultados.
    """
    # Validar datos del terreno
    try:
        datos_terreno = pandas.DataFrame(terreno_data)
        datos_cultivos = pandas.DataFrame(cultivos_data)
        
        dias_requeridos = set(range(1, 181))
        if not set(datos_terreno['dia']).issuperset(dias_requeridos):
            faltantes = dias_requeridos - set(datos_terreno['dia'])
            return {"error": f"Faltan días en datos_terreno: {faltantes}"}
        
        columnas_requeridas = ['dia', 'temperatura', 'promedio_precipitaciones', 'humedad_suelo']
        if not all(col in datos_terreno.columns for col in columnas_requeridas):
            faltantes = [col for col in columnas_requeridas if col not in datos_terreno.columns]
            return {"error": f"Faltan columnas en datos_terreno: {faltantes}"}
        
        for col in ['temperatura', 'promedio_precipitaciones', 'humedad_suelo']:
            if not pandas.api.types.is_numeric_dtype(datos_terreno[col]):
                return {"error": f"Columna {col} en datos_terreno contiene valores no numéricos"}
        
        # Validar datos de cultivos
        columnas_cultivos = ['cultivo', 'duracion_crecimiento', 'necesidad_agua_vegetativa', 
                             'necesidad_agua_floracion', 'necesidad_nutrientes', 'dificultad_cultivo', 
                             'precio_mercado', 'costo_agua', 'costo_fertilizante']
        if not all(col in datos_cultivos.columns for col in columnas_cultivos):
            faltantes = [col for col in columnas_cultivos if col not in datos_cultivos.columns]
            return {"error": f"Faltan columnas en datos_cultivos: {faltantes}"}
        
        for col in columnas_cultivos[1:]:
            if not pandas.api.types.is_numeric_dtype(datos_cultivos[col]):
                return {"error": f"Columna {col} en datos_cultivos contiene valores no numéricos"}
    
    except Exception as e:
        return {"error": f"Error al procesar datos: {str(e)}"}

    # Seleccionar optimizador y función
    algoritmo = 0  # GSA
    funcion_objetivo = 0  # FitnessAgricola
    detalles_funcion = fr.obtener_detalles_funcion(funcion_objetivo)
    
    # Ejecutar GSA
    fr.establecer_datos(datos_terreno, datos_cultivos)
    x = gsa.GSA(getattr(fr, detalles_funcion[0]), detalles_funcion[1], detalles_funcion[2], 
                detalles_funcion[3], tamano_poblacion, iteraciones)
    
    # Preparar resultados
    mejor_solucion = x.bestIndividual
    mejor_ganancia = -x.convergence[-1]
    cultivo_seleccionado = datos_cultivos.iloc[int(round(mejor_solucion[0]))]['cultivo']
    fecha_siembra = int(round(mejor_solucion[1]))
    programa_riego = mejor_solucion[2:12].tolist()
    fecha_cosecha = int(round(mejor_solucion[1] + datos_cultivos.iloc[int(round(mejor_solucion[0]))]['duracion_crecimiento'] + mejor_solucion[12]))
    dosis_abono = mejor_solucion[13:].tolist()
    
    # Generar gráfico de convergencia
    plt.figure(figsize=(8, 6))
    plt.plot(-x.convergence)
    plt.title("Curva de Convergencia del GSA")
    plt.xlabel("Iteración")
    plt.ylabel("Ganancia Neta ($)")
    plt.grid(True)
    
    # Guardar gráfico como imagen en memoria
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Preparar resultados en JSON
    resultado = {
        "status": "success",
        "optimizador": x.Algorithm,
        "funcion_objetivo": x.objectivefunc,
        "inicio": x.startTime,
        "fin": x.endTime,
        "tiempo_ejecucion": x.executionTime,
        "curva_convergencia": [-val for val in x.convergence.tolist()],
        "estrategia_optima": {
            "cultivo_seleccionado": cultivo_seleccionado,
            "fecha_siembra": fecha_siembra,
            "programa_riego_mm_cada_10_dias": programa_riego,
            "fecha_cosecha": fecha_cosecha,
            "dosis_abono_organico_kg_ha_cada_10_dias": dosis_abono,
            "ganancia_estimada_usd": round(mejor_ganancia, 2)
        },
        "grafico_convergencia": f"data:image/png;base64,{img_base64}"
    }
    
    return resultado