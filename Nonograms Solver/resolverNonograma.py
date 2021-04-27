#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Archivo: resolverNonograma.py
# 
# Descripción: Este archivo es el programa principal, y es el que debe invocar
#              el usuario.
#
# Integrantes:
#     - Fabio Suárez     (12-10578)
#     - Ronald Becerra   (12-10706)
#     - Constanza Abarca (13-10000)

from funcionesParaSATsolver import *

def main():

    # Leer el archivo de entrada
    try:
        nombreArchivoEntrada = sys.argv[1]
        rutaArchivoEntrada = globales.rutaEntradaPrograma +nombreArchivoEntrada
        archivoEntrada = open(rutaArchivoEntrada)
        nombre = str(nombreArchivoEntrada).split(".")[0]
    except:
        print(">>> ERROR: El archivo especificado no existe.")
        sys.exit()
    
    # Se crearán los directorios (si no existen) para ir almacenando las salidas
    crearDirectorios() 

    lineasTotales = []

    for lineaPrev in archivoEntrada:
        linea = lineaPrev.split("\n")
        lineasTotales.append(linea)
        
    archivoEntrada.close()

    # Determinar el total de filas y el total de columnas
    totColumnas = 0
    totFilas = 0
    linea0 = lineasTotales[0][0].split(" ")
    linea1 = lineasTotales[1][0].split(" ")

    if linea0[0] == "width":
        totColumnas = int(linea0[1])
    else:
        totFilas = int(linea0[1])

    if linea1[0] == "height":
        totFilas = int(linea1[1])
    else:
        totColumnas = int(linea1[1])

    try:
        assert(totFilas > 0 and totColumnas > 0)
    except:
        print(">>>ERROR: Archivo de entrada inválido.")
        sys.exit()

    # Leer la cantidad de elementos por bloque, tanto en las filas como en las columnas
    leerFilas = []
    leerColumnas = []
    primeroFilas = (lineasTotales[2][0] == "rows")
    totLineas = len(lineasTotales)
    i = 3

    #=== Puede ser que el archivo primero especifique las filas
    if primeroFilas:
        while(lineasTotales[i][0] != "columns"):
            nuevaFila = []
            nuevaLineaLeer = lineasTotales[i][0].split(",")
            for elem in nuevaLineaLeer:
                if (elem != "") and (elem != " "):
                    nuevaFila.append(int(elem))
            leerFilas.append(nuevaFila)
            i += 1
        i += 1
        for j in range(i,totLineas):
            nuevaColumna = []
            nuevaLineaLeer = lineasTotales[j][0].split(",")
            for elem in nuevaLineaLeer:
                if (elem != "") and (elem != " "):
                    nuevaColumna.append(int(elem))
            leerColumnas.append(nuevaColumna)
    #=== Caso en que el archivo primero especifica las columnas
    else:
        while(lineasTotales[i][0] != "rows"):
            nuevaColumna = []
            nuevaLineaLeer = lineasTotales[i][0].split(",")
            for elem in nuevaLineaLeer:
                if (elem != "") and (elem != " "):
                    nuevaColumna.append(int(elem))
            leerColumnas.append(nuevaColumna)
            i += 1
        i += 1
        for j in range(i,totLineas):
            nuevaFila = []
            nuevaLineaLeer = lineasTotales[j][0].split(",")
            for elem in nuevaLineaLeer:
                if (elem != "") and (elem != " "):
                    nuevaFila.append(int(elem))
            leerFilas.append(nuevaFila)
            
    generarArchivoGlucosa(nombre, leerFilas, leerColumnas, totFilas, totColumnas)

    # Agarramos el archivo generado en la forma CNF DIMACS y procedemos a ejecutarlo con el Sat solver de Glucose
    correrGlucose(nombre)

    # Genera archivo txt con la matriz de bits y archivo bitmap
    transformarABitmap(nombre, totFilas, totColumnas)
                
if __name__ == '__main__':
    main()   
