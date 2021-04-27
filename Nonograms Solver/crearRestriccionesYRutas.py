#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Archivo: crearRestricciones.py
# 
# Descripción: Archivo que contiene las funciones que serán usadas por el archivo
#              resolverNonograma.py para generar las restricciones (las reglas).
#              Además, almacena las variables globales que utilizarán los otros
#              códigos.
#
# Integrantes:
#     - Fabio Suárez     (12-10578)
#     - Ronald Becerra   (12-10706)
#     - Constanza Abarca (13-10000)

import os
# Clase que permite almacenar variables globales necesarias para todo el programa
class globales():
    # Contadores
    contadorVariables = 0
    contadorClausulas = 0
    # Rutas
    rutaActual = os.getcwd()
    rutaEjecutableGlucosa = rutaActual + "/glucose-syrup-4.1/simp/glucose" # >>>> Esta ruta posiblemente haya que modificarla
    rutaEntradaPrograma = rutaActual + "/nonogramas/"
    rutaEntradaGlucosa = rutaActual + "/Entrada Para Glucose/"
    rutaSalidaGlucosa = rutaActual + "/Salida SAT Glucose/"
    rutaEstadisticas = rutaActual + "/Estadisticas-Glucose/"
    rutaResultadoTxt = rutaActual + "/txt-salida-matriz-PBM/"
    rutaPBMs = rutaActual + "/PBMs/"
    
globales = globales()

# Crear los directorios necesarios
def crearDirectorios():
    try: 
        os.mkdir(globales.rutaEntradaGlucosa)
    except:
        pass
    try:
        os.mkdir(globales.rutaSalidaGlucosa)
    except:
        pass
    try:
        os.mkdir(globales.rutaEstadisticas)
    except:
        pass
    try:
        os.mkdir(globales.rutaResultadoTxt)
    except:
        pass
    try:
        os.mkdir(globales.rutaPBMs)
    except:
        pass

# Función para ir generando un identificador distinto a cada variable que se cree
def generarVariable():
    globales.contadorVariables += 1    
    return globales.contadorVariables

def imprimirVariable(v):
    return str(v)

# Función que devuelve dos matrices: (1) la de variables Q para filas y (2) las de variables Q para columnas
def matrizVariablesQ(leerFilas,leerColumnas,totFilas,totColumnas):
    
    # Creamos las variables para las filas [[1,4],[2,3]]
    variablesParaFilas = []
    numBloque = 0
    for fila in leerFilas:  # Las filas serían [1,4] y [2,3]    
        for bloque in fila: # Los bloques serían el 1 y el 4 para la primera fila
            variablesParaBloque = []
            # Caso en que no aparece ningún bloque en una fila
            if bloque == 0:
                variablesParaBloque.append([])
            for i in range(bloque):                
                variablesParaBloque.append(list(generarVariable() for k in range(totColumnas)))
            variablesParaFilas.append(variablesParaBloque)
            numBloque += 1

    # Creamos las variables para las columnas [[1,4],[2,3]]
    variablesParaColumnas = []
    numBloque = 0
    for columna in leerColumnas:  # Las columnas serían [1,4] y [2,3]       
        for bloque in columna:    # Los bloques serían el 1 y el 4 para la primera columna
            variablesParaBloque = []
            # Caso en que no aparece ningún bloque en una columna
            if bloque == 0:
                variablesParaBloque.append([])
            for i in range(bloque):
                variablesParaBloque.append(list(generarVariable() for k in range(totFilas)))
            variablesParaColumnas.append(variablesParaBloque)
            numBloque += 1

    return variablesParaFilas, variablesParaColumnas

# Función que devuelve una matriz con las variables pi
def matrizVariablesP(totFilas,totColumnas):
    matriz = []
    for i in range(totFilas):
        nuevaFila = []
        for j in range(totColumnas):
            nuevaFila.append(generarVariable())
        matriz.append(nuevaFila)

    return matriz

# Función para crear todas las restricciones
def restricciones(variablesParaFilas,variablesParaColumnas,totFilas,totColumnas,matrizP,leerFilas,leerColumnas):
    
    string = ""  # Cadena de caracteres retornada por esta función

    
    #************************************* Restricciones para las filas *****************************************
    # ===========================================================================================================

        
    # 1) Si se pinta la primera Q del bloque, se deben pintar las siguientes
    #    FÓRMULA GENERAL: ( Q0,i => Q1,i+1 && Q2,i+2 )
    #    FÓRMULA EN CNF:  (¬Q0,i v Q1,i+1) && (¬Q0,i v Q2,i+2)    
    for variablesParaBloque in variablesParaFilas:
        if (variablesParaBloque[0]!=[]):
            q_necesarias = len(variablesParaBloque)
            for j in range(1,q_necesarias):
                if (variablesParaBloque[j]!=[]): 
                    for i in range(totColumnas - q_necesarias + 1):
                        string += "-"+imprimirVariable(variablesParaBloque[0][i])+" "+imprimirVariable(variablesParaBloque[j][i+j])+" 0\n"
                        globales.contadorClausulas += 1

    # 2) Restricciones de solamente 1
    # ===============================

    #=== 2.1) Al menos 1
    for variablesParaBloque in variablesParaFilas:
        for lista in variablesParaBloque:
            if lista != []:  
                for var in lista:
                    string += imprimirVariable(var)+" "
                string += " 0\n"
                globales.contadorClausulas += 1

    #=== 2.2) A lo sumo 1
    for variablesParaBloque in variablesParaFilas:
        long = len(variablesParaBloque[0])
        for lista in variablesParaBloque:
            if lista != []:  
                for i in range(long-1):
                    for j in range(i+1,long):
                        string += "-"+imprimirVariable(lista[i])+" -"+imprimirVariable(lista[j])+" 0\n"
                        globales.contadorClausulas += 1

    # Por comodidad, vamos a agrupar los bloques de una misma fila
    numBloqueActual = 0
    filasTotales = []
    for i in range(totFilas):                # Va iterando sobre las filas
        filaActual = []
        for j in range(len(leerFilas[i])):   # El tope del rango es la cantidad de bloques en la fila
            filaActual.append(variablesParaFilas[numBloqueActual])
            numBloqueActual += 1
        filasTotales.append(filaActual)

    # 3) Pintar las variables P según las variables Q    FÓRMULA GENERAL: ( Pi <=> Q0,i v Q1,i v Q2,i )
    # =============================================== 

    #=== 3.1) FÓRMULA PREVIA: ( Pi => Q0,i v Q1,i v Q2,i )      FÓRMULA EN CNF: ( ¬Pi v Q0,i v Q1,i v Q2,i )  
    for i in range(totFilas):        
        for k in range(totColumnas):
            string += "-"+imprimirVariable(matrizP[i][k])
            for bloque in filasTotales[i]:
                for lista in bloque:
                    if lista != []:
                        string += " "+imprimirVariable(lista[k])
            string += " 0\n"
            globales.contadorClausulas += 1

    #=== 3.2) FÓRMULA PREVIA: ( (Q0,i v Q1,i v Q2,i) => Pi )    FÓRMULA EN CNF: ( (¬Q0,i v Pi) && (¬Q1,i v Pi) && (¬Q2,i v Pi) ) 
    for i in range(totFilas):        
        for k in range(totColumnas):
            for bloque in filasTotales[i]:
                for lista in bloque:
                    if lista != []:
                        string += " -"+imprimirVariable(lista[k])+" "+imprimirVariable(matrizP[i][k])+" 0\n"
                        globales.contadorClausulas += 1

    # 4) Hacer que los bloques no se solapen ni aparezcan contiguos
    # =============================================================
    for fila in filasTotales:
        long = len(fila)
        for i in range(long-1):               # Se refiere al bloque que termina
            tamBloque = len(fila[i])-1        # Cantidad de elementos en el bloque, restado en 1
            if (fila[i][tamBloque] != []):
                for k in range(totColumnas-1):    # Se refiere a la variable del bloque que termina
                    for j in range(i+1,long):     # Se refiere al bloque que comienza
                        if(fila[j][0]!=[]):
                            for s in range(k+2):      # Se refiere a la variable del bloque que comienza
                                string += "-"+imprimirVariable(fila[i][tamBloque][k])+" -"+imprimirVariable(fila[j][0][s])+" 0\n"
                                globales.contadorClausulas += 1

    # 5) Hacer que el elemento i-ésimo de un bloque no aparezca antes que el i-1-ésimo
    # ================================================================================
    for fila in filasTotales:
        for bloque in fila:
            tamBloque = len(bloque)
            for i in range(tamBloque-1):
                if (bloque[i] != []):
                    for pos in range(totColumnas):
                        for j in range(i+1,tamBloque):
                            if(bloque[j] != []):
                                for k in range(pos+1):
                                    string += "-"+imprimirVariable(bloque[i][pos])+" -"+imprimirVariable(bloque[j][k])+" 0\n"
                                    globales.contadorClausulas += 1


    #************************************ Restricciones para las columnas ***************************************
    # ===========================================================================================================


    # 1) Si se pinta la primera Q del bloque, se deben pintar las siguientes
    #    FÓRMULA GENERAL: ( Q0,i => Q1,i+1 && Q2,i+2 )
    #    FÓRMULA EN CNF:  (¬Q0,i v Q1,i+1) && (¬Q0,i v Q2,i+2)
    for variablesParaBloque in variablesParaColumnas:
        if (variablesParaBloque[0]!=[]):
            q_necesarias = len(variablesParaBloque)
            for j in range(1,q_necesarias):
                if (variablesParaBloque[j]!=[]):
                    for i in range(totFilas - q_necesarias + 1):
                        string += "-"+imprimirVariable(variablesParaBloque[0][i])+" "+imprimirVariable(variablesParaBloque[j][i+j])+" 0\n"
                        globales.contadorClausulas += 1

    # 2) Restricciones de solamente 1
    # ===============================

    #=== 2.1) Al menos 1
    for variablesParaBloque in variablesParaColumnas:
        for lista in variablesParaBloque:
            if lista != []: 
                for var in lista:
                    string += imprimirVariable(var)+" "
                string += " 0\n"
                globales.contadorClausulas += 1

    #=== 2.2) A lo sumo 1
    for variablesParaBloque in variablesParaColumnas:
        long = len(variablesParaBloque[0])
        for lista in variablesParaBloque:
            if lista != []:
                for i in range(long-1):
                    for j in range(i+1,long):
                        string += "-"+imprimirVariable(lista[i])+" -"+imprimirVariable(lista[j])+" 0\n"
                        globales.contadorClausulas += 1

    # Por comodidad, vamos a agrupar los bloques de una misma columna
    numBloqueActual = 0
    columnasTotales = []
    for i in range(totColumnas):              # Va iterando sobre las columnas
        columnaActual = []
        for j in range(len(leerColumnas[i])): # El tope del rango es la cantidad de bloques en la columna
            columnaActual.append(variablesParaColumnas[numBloqueActual])
            numBloqueActual += 1
        columnasTotales.append(columnaActual)

    # 3) Pintar las variables P según las variables Q    FÓRMULA GENERAL: ( Pi <=> Q0,i v Q1,i v Q2,i )
    # =============================================== 

    #=== 3.1) FÓRMULA PREVIA: ( Pi => Q0,i v Q1,i v Q2,i )      FÓRMULA EN CNF: ( ¬Pi v Q0,i v Q1,i v Q2,i )  
    for i in range(totColumnas):        
        for k in range(totFilas):
            string += "-"+imprimirVariable(matrizP[k][i])
            for bloque in columnasTotales[i]:
                for lista in bloque:
                    if lista != []:
                        string += " "+imprimirVariable(lista[k])
            string += " 0\n"
            globales.contadorClausulas += 1    

    #=== 3.2) FÓRMULA PREVIA: ( (Q0,i v Q1,i v Q2,i) => Pi )    FÓRMULA EN CNF: ( (¬Q0,i v Pi) && (¬Q1,i v Pi) && (¬Q2,i v Pi) ) 
    for i in range(totColumnas):        
        for k in range(totFilas):
            for bloque in columnasTotales[i]:
                for lista in bloque:
                    if lista != []:
                        string += " -"+imprimirVariable(lista[k])+" "+imprimirVariable(matrizP[k][i])+" 0\n"
                        globales.contadorClausulas += 1

    # 4) Hacer que los bloques no se solapen ni aparezcan contiguos
    # =============================================================
    for columna in columnasTotales:
        long = len(columna)
        for i in range(long-1):               # Se refiere al bloque que termina
            tamBloque = len(columna[i])-1     # Cantidad de elementos en el bloque, restado en 1
            if (columna[i][tamBloque] != []):
                for k in range(totFilas-1):       # Se refiere a la variable del bloque que termina
                    for j in range(i+1,long):     # Se refiere al bloque que comienza
                        if(columna[j][0] != []):
                            for s in range(k+2):      # Se refiere a la variable del bloque que comienza                        
                                string += "-"+imprimirVariable(columna[i][tamBloque][k])+" -"+imprimirVariable(columna[j][0][s])+" 0\n"
                                globales.contadorClausulas += 1
                                
    # 5) Hacer que el elemento i-ésimo de un bloque no aparezca antes que el i-1-ésimo
    # ================================================================================
    for columna in columnasTotales:
        for bloque in columna:
            tamBloque = len(bloque)
            for i in range(tamBloque-1):
                if (bloque[i] != []):
                    for pos in range(totFilas):
                        for j in range(i+1,tamBloque):
                            if (bloque[j]!=[]):
                                for k in range(pos+1):                                     
                                    string += "-"+imprimirVariable(bloque[i][pos])+" -"+imprimirVariable(bloque[j][k])+" 0\n"
                                    globales.contadorClausulas += 1

    # Devolver resultado
    return string
