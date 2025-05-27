# -*- coding: utf-8 -*-
"""
Código Python del Algoritmo de Búsqueda Gravitacional (GSA)
Propósito: Calcular la constante gravitacional
"""

import numpy

def gConstant(iteracion, iteraciones):
    alfa = 10  # Reducido para mayor exploración
    G0 = 200   # Aumentado para mayor fuerza inicial
    Gimd = numpy.exp(-alfa * float(iteracion) / iteraciones)
    G = G0 * Gimd
    return G