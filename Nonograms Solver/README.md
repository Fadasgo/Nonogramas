# Objetivo
El objetivo del proyecto es construir un solucionador de juegos *Nonogramas*
(ver http://www.nonograms.org/) utilizando un *SAT solver*.

El esquema del solucionador es el siguiente. Dado un nonograma, se tiene
que construir una teor&iacute;a proposicional &Delta; tal que:
* el nonograma tiene soluci&oacute;n si y s&oacute;lo si &Delta; es satisfacible,
* las soluciones del nonograma est&aacute;n en correspondencia con los modelos de &Delta;.

El solucionador consiste entonces de:
1. un programa que *codifica* un nonograma dado en una teor&iacute;a proposicional &Delta;,
2. llamar a un SAT solver con entrada &Delta;,
3. si el SAT solver consigue un modelo, llama un programa que *decodifica* el modelo en una soluci&oacute;n para el nonograma.

# Material entregado

Se entrega un directorio que contiene distintos casos de prueba.

# Actividad 1

Instalar el SAT solver llamado ```glucose``` (https://www.labri.fr/perso/lsimon/glucose/)
y estudiar el formato de entrada y salida del mismo.

# Actividad 2

Estudiar los nonogramas y el formato .non para describirlos. Construir un codificador de nonogramas en teor&iacute;as proposicionales,
y un decodificador de modelos proposicionales en soluciones al nonograma.

# Actividad 3

Construir un ejecutable que dado un archivo con un caso de prueba, llama al codificador
sobre el caso de entrada, luego llama al SAT solver, y por &uacute;ltimo decodifica la
soluci&oacute;n calculada (si existe) en una soluci&oacute;n al nonograma.

# Actividad 4

Construir una imagen a partir de la soluci&oacute;n al nonograma, ya que toda
soluci&oacute;n se corresponde con un bitmap de pixels blanco y negro.

# Entregables

Se debe entregar, en el repositorio, todo el c&oacute;digo implementado,
los resultados experimentales, y un peque&ntilde;o informe, preferiblemente
en formato .md, que describa lo que hicieron y sus conclusiones.

