# -*- coding: utf-8 -*-
"""
Código Python del Algoritmo de Búsqueda Gravitacional (GSA)
Propósito: Implementar el GSA para minimizar la función objetivo
"""

import random
import numpy
import math
from solution import solution
import time
import massCalculation
import gConstant
import gField
import move

def GSA(func_objetivo, lim_inferior, lim_superior, dimension, tamano_poblacion, iteraciones):
    # Parámetros del GSA
    control_elitista = 1
    potencia_r = 1

    s = solution()

    """ Inicializaciones """
    velocidades = numpy.zeros((tamano_poblacion, dimension))
    fitness = numpy.zeros(tamano_poblacion)
    masas = numpy.zeros(tamano_poblacion)
    mejor_global = numpy.zeros(dimension)
    mejor_fitness_global = float("inf")

    # Convertir límites a arreglos NumPy
    lim_inferior = numpy.array(lim_inferior)
    lim_superior = numpy.array(lim_superior)

    # Inicialización más enfocada en regiones válidas
    posiciones = numpy.zeros((tamano_poblacion, dimension))
    posiciones[:, 0] = numpy.random.randint(0, 3, tamano_poblacion)  # id_cultivo: 0, 1, 2
    posiciones[:, 1] = numpy.random.uniform(1, 30, tamano_poblacion)  # fecha_siembra
    posiciones[:, 2:12] = numpy.random.uniform(0, 50, (tamano_poblacion, 10))  # riego
    posiciones[:, 12] = numpy.random.uniform(-10, 10, tamano_poblacion)  # desplazamiento_cosecha
    posiciones[:, 13:] = numpy.random.uniform(0, 20, (tamano_poblacion, 10))  # fertilizante

    curva_convergencia = numpy.zeros(iteraciones)

    print(f"GSA está optimizando \"{func_objetivo.__name__}\"")

    tiempo_inicio = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")

    for l in range(0, iteraciones):
        for i in range(0, tamano_poblacion):
            pos_clip = numpy.clip(posiciones[i, :], lim_inferior, lim_superior)
            posiciones[i, :] = pos_clip

            # Calcular función objetivo
            fitness[i] = func_objetivo(pos_clip)

            if mejor_fitness_global > fitness[i]:
                mejor_fitness_global = fitness[i]
                mejor_global = pos_clip

        """ Calcular Masas """
        masas = massCalculation.massCalculation(fitness, tamano_poblacion, masas)

        """ Calcular Constante Gravitacional """
        G = gConstant.gConstant(l, iteraciones)

        """ Calcular Campo Gravitacional """
        aceleraciones = gField.gField(tamano_poblacion, dimension, posiciones, masas, l, iteraciones, G, control_elitista, potencia_r)

        """ Actualizar Posiciones """
        posiciones, velocidades = move.move(tamano_poblacion, dimension, posiciones, velocidades, aceleraciones)

        curva_convergencia[l] = mejor_fitness_global

        if l % 1 == 0:
            print([f'En iteración {l+1} la mejor fitness es {mejor_fitness_global}'])

    tiempo_fin = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = tiempo_fin - tiempo_inicio
    s.convergence = curva_convergencia
    s.Algorithm = "GSA"
    s.objectivefunc = func_objetivo.__name__

    s.bestIndividual = mejor_global
    return s