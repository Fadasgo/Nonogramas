#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Archivo: funcionesParaSATsolver.py
#
# Descripción: Archivo que contiene las funciones necesarias para que nuestro programa
#              interactúe con el SAT solver glucosa (que debe estar en el mismo directorio
#              de este código).
#
# Integrantes:
#     - Fabio Suárez     (12-10578)
#     - Ronald Becerra   (12-10706)
#     - Constanza Abarca (13-10000)

import sys
import subprocess
from crearRestriccionesYRutas import *

# Crea un archivo con la entrada que será leída por el SAT solver
def generarArchivoGlucosa(nombreArchivo,leerFilas,leerColumnas,totFilas,totColumnas):

    # Crear la matriz de variables P (las que determinan si una casilla está pintada o no)
    matrizP = matrizVariablesP(totFilas,totColumnas) 

    # Crear la matriz de variables Q (las auxiliares)
    (variablesFilas,variablesColumnas) = matrizVariablesQ(leerFilas,leerColumnas,totFilas,totColumnas)

    # Generar la cadena de caracteres con las restricciones
    string = restricciones(variablesFilas,variablesColumnas,totFilas,totColumnas,matrizP,leerFilas,leerColumnas)

    # A esa cadena de caracteres añadirle al principio los parámetros para que los pueda leer el SAT solver
    string = "p cnf "+str(globales.contadorVariables)+" "+str(globales.contadorClausulas)+"\n"+string
    
    # Crear el archivo donde se guardará la cadena de caracteres que acabamos de hacer
    f = open(globales.rutaEntradaGlucosa + nombreArchivo + " - CNF.txt","w", encoding="utf-8")

    # Escribir la cadena de caracteres en ese archivo
    f.write(string)
    f.close()

# Ejecuta el sat solver de glucose con los archivos CNF DIMACS generados anteriormente
def correrGlucose(nombreArchivo):
    rutaEntrada = globales.rutaEntradaGlucosa + nombreArchivo + " - CNF.txt" # Archivo que se le pasará como entrada a Glucose
    rutaSalida = globales.rutaSalidaGlucosa+ nombreArchivo + " - SAT.txt"    # Archivo que devolverá la ejecución de Glucose
    archivoSalida = open(rutaSalida, "w")
    # Crea el archivo f donde se guarda el output de la terminal
    # Por otro lado se guarda la salida de la satifacibilidad de los valores en el archivo contenido en la variable rutaSalida
    with open(globales.rutaEstadisticas + nombreArchivo + " - estadísticas.txt", "w") as f:
        subprocess.call([globales.rutaEjecutableGlucosa, rutaEntrada, rutaSalida], stdout = f)
    #subprocess.call([globales.rutaActual + "/glucose-syrup-4.1/simp/glucose", rutaEntrada, rutaSalida])

    #f.close()
    archivoSalida.close()

# Guarda en un txt matriz de salida de bits en caso de ser satisfacible.
# En caso contrario crea un archivo que contiene la notificación UNSAT
def transformarABitmap(nombre, totFilas, totColumnas):

    # Encontramos la ruta del archivo que generó Glucose
    file = open(globales.rutaSalidaGlucosa + nombre + " - SAT.txt" , "r")
    lectura = file.readline()
    txt = open(globales.rutaResultadoTxt + nombre + " - resultado.txt", "w")

    if lectura == "UNSAT\n":
        print("El problema del archivo "+str(archivoLeer)+" no es satisfacible.\n")
        txt.write("UNSAT \n")
        txt.close()
        file.close()

    else:
        bitmap = open(globales.rutaPBMs + nombre + " - imagen.pbm", "w")
        bitmap.write("P1\n"+ str(totColumnas)+" "+str(totFilas)+"\n")
        txt.write("P1\n"+ str(totColumnas)+" "+str(totFilas)+"\n")

        variables = lectura.split(" ")
        lista = [] # Contendrá los valores de las variables Pi, que indican si
                   # la casilla va encendida o apagada.
        for i in range(totFilas * totColumnas):
            lista.append(int(variables[i]))     

        x = 0
        for i in range(totFilas):
            for j in range(int(totColumnas)):
                if(lista[x] > 0):
                    bitmap.write("1 ")
                    txt.write("1 ")
                else:
                    bitmap.write("0 ")
                    txt.write("0 ")
                x += 1
            bitmap.write("\n")
            txt.write("\n")


        file.close()
        bitmap.close()
        txt.close()
