# -*- coding: utf-8 -*-
"""Entrega - IA - Clasificacicón - Andersson--Bertino.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j7OE5u1Acv94RcCl_2xZrYeJ03sXNrPH

# Técnicas de Clasificación

Seleccionar en https://www.openml.org/ un dataset. Teniendo en cuenta dicho dataset, resolver los siguiente puntos:

>a) Definir cuál es el objetivo de aplicar técnicas de clasificación.

>b) En caso de ser necesario, definir qué pre‐procesamiento se realizará a los datos. Justificar.

>d) Obtener dos clasificadores utilizando la librería Scikit learn. Para ello elegir 2 técnicas de clasificación, configurar los clasificadores, detallar de qué forma se evaluarán los clasificadores (hold-out / cross-validation), ejecutar los algoritmos. Justificar las decisiones tomadas.

>e) Evaluar los dos clasificadores y compararlos, indicando cual de los dos recomendaría.

>f) Explicar un ejemplo de cómo los clasificadores obtenidos pueden ser usados en elfuturo.

dataset utilizado: https://www.openml.org/d/12

El dataset utilizado es uno de una colección de 6, que consiste en la descripción de características de dígitos numéricos (0 a 9) escritos a mano, extraídos de mapas de utilidad daneses. Los patrones correspondientes en los distintos datasets corresponden al mismo dígito original. El valor de cada atributo (attrX) representa la correlacion entre ese atributo y una imagen de un mapa. Este dataset consiste de 200 ejemplos de 10 clases distintas dando un total de 2000 ejemplos para desarrollar un analisis. No se ofrece mas informacion del significado del dataset por parte de la fuente que nos lo brinda (OpenML)

>a) El objetivo de aplicar técnicas de clasificación es organizar y separar los datos en diferentes categorías. Cada categoría puede ser definida arbitariamente con características determindas.
"""

# basar analisis en arboles de decisiion, clasiicador bayesiano y vecinos mas cercanos y despues ver otros, naive-bayes

# soporte para cargar dataset de https://www.openml.org/
!pip install openml
import numpy as np
import openml
import pandas as pd                                            #Librería Pandas
from sklearn.tree import DecisionTreeClassifier                #Arboles de decision
from sklearn.naive_bayes import MultinomialNB                  #Naive-Bayes Multinomial
from sklearn import neighbors                                  #KNN vecinos mas cercanos
from sklearn.pipeline import Pipeline                          #Mecanismo para Pipeline
from sklearn.model_selection import train_test_split           #Mecanismo para realizar hold-out
from sklearn.metrics import confusion_matrix                   #Servicios relacionados a la matriz de confusión
from sklearn.metrics import classification_report              #Provee analisis de métricas de evaluación
from sklearn.model_selection import cross_val_score            #Validacion cruzada
from sklearn.model_selection import StratifiedKFold            #Diferentes metodos de K fold  cross validation
from sklearn.model_selection import KFold
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import StratifiedShuffleSplit

#Defino algunos colores para imprimir mejor las cosas

negro    = '\u001b[30m'
rojo     = '\u001b[31m'
verde    = '\u001b[32m'
amarillo = '\u001b[33m'
azul     = '\u001b[34m'
magenta  = '\u001b[35m'
cyan     = '\u001b[36m'
blanco   = '\u001b[37m'
reset    = '\u001b[0m'

# indicamos cual dataset queremos utilizar, en este caso el nro. 12
dataset = openml.datasets.get_dataset(12)

# separamos las información almacenada en el dataset
# datos = tuplas sin la clase
# clases = clase i asociada a la tupla i

datos, clases, categorical_indicator, attribute_names = dataset.get_data(
    dataset_format='dataframe',
    target=dataset.default_target_attribute )

#  concatenamos la información relevante en un único DataFrame 
df = pd.concat([datos, clases], axis=1)

# La función train_test_split permite dividir los datos
# en 4 partes, en dos conjuntos de trabajo una de entrenamiento
# y otro de prueba, con sus respectivas clases o categorias reales
# Esto es hold-out (proceso de dividir los ejemplos iniciales)
# shuffle = True permite que se tomen al azar los ejemplos
datosEntrenamiento, datosPrueba, clasesRealesDEntre,clasesRealesDPrueba = train_test_split(datos, clases, test_size=0.25, shuffle= True)

# Se tomó un 75% de los ejemplo como conjunto de entrenamiento y
# y el 25% restante como conjunto de prueba, ya que normalmente
# se suele usar 80/20, optamos por brindarle a los algorítmos
# un poco mas de ejemplor de prueba

""">b) Procesamiento usado:

* Generar uns lista con las clases del dataset, para poder operar en los diferentes algorítmos
"""

# Convertir las clases a lista
clasesAux = list(clases)
print(clasesAux)

# Convertir lista a conjunto
clasesAux2 = set(clasesAux)
print(clasesAux2)

# Ordenar elementos
clasesAux3 = list(clasesAux2)
l = list()
for i in clasesAux3:
  l.append(int(i))
l.sort()
print(l)

# Reconvertir clases a texto
del clasesAux3[:]
for i in l:
  clasesAux3.append(str(i))

print(clasesAux3)

# Definición de clasificadores
# Aclaracion del Profe Ariel:
# --> Con que comparen 2 clasificadores con parámetros base está bien.

arbDecision = DecisionTreeClassifier()                 # Arbol de decisión, ver si es necesario hacerlo
nbMultinomial = MultinomialNB()                        # Naive-Bayes Multinomial 
vecinosMasCerca = neighbors.KNeighborsClassifier()     # KNN - Vecinos más cercanos

# Muestro los parámetro de los clasificadores
print(" Hiperparámetros de los distintos clasificadores: ")
print(amarillo,nbMultinomial,reset)
print(azul,vecinosMasCerca,reset)
print(verde,arbDecision,reset)

# Función que dado un clasificador, los datos y sus clases
# Se lo entrena para que pueda predecir futuros ejemplos
# Tambien se realiza un promedio entre las clases reales y 
# las clases predecidas con el fin de medir el porcentaje
# de exito en la clasificación

def oraculoDeDelfos(clasificador, dato, clases):
  print(negro,"--------------------------------------------------------------------------------------------------------------------------------",reset)
  print(azul,"Clasificador usado: ",clasificador,reset)
  p = clasificador.fit(dato, clases)                                                         #entrenar el clasificador
  predecido =p.predict(dato)                                                                 #predecir
  mediaDeAcierto = "{0:.3f}".format(np.mean(predecido == clases) * 100)                       #format me permite mostrar una cantidad de decimales dada
  print(verde,"Clases obtenidas:",predecido, ", Porcentaje de exito:", mediaDeAcierto, "%",reset)
  print(negro,"--------------------------------------------------------------------------------------------------------------------------------"+reset)

oraculoDeDelfos(nbMultinomial, datosEntrenamiento, clasesRealesDEntre)
oraculoDeDelfos(vecinosMasCerca, datosEntrenamiento, clasesRealesDEntre)
oraculoDeDelfos(arbDecision, datosEntrenamiento, clasesRealesDEntre)

"""Se puede observar que si bien el clasificador basado en árbol de decisión tiene 100% de precision, no sería útil en noestro caso. El clasificador se ajustó demasiado a los datos(overffiting), con lo cuál a la hora de clasificar nuevos ejemplos lo más probable es que los clasifique mal. por este motivo continuaremos el análisis con los clasificadores naive-bayes multinomial y el KNN. """

# en proceso de adaptacion

# Construcción de la matriz de confusión

# Función que predice las clases 

def predecir(cladificador, datosEntrenaReales, clasesEntrenaReales, datosPrueba):
  pipe = Pipeline([ ('CLASIFICADOR', cladificador) ])
  pipe = pipe.fit(datosEntrenaReales, clasesEntrenaReales)     #entrenamiento
  predicho = pipe.predict(datosPrueba)                         #predicción
  return (predicho)

predichoNB  = predecir(nbMultinomial, datosEntrenamiento, clasesRealesDEntre, datosPrueba)
predichoKNN = predecir(vecinosMasCerca, datosEntrenamiento, clasesRealesDEntre, datosPrueba)
predichoARB = predecir(arbDecision, datosEntrenamiento, clasesRealesDEntre, datosPrueba)

# Función que genera la matriz de confusión a partir de 
# las clases reales de pruba generadas con hold-out
# y las clases predichas por el clasificador usado

def generarMConfusion(clases, predecido):
  print(negro,"--------------------------------------------------------------------------------------------------------------------------------",reset)
  matrizConfusion = confusion_matrix(clases, predecido)
  print(amarillo)
  print("Matriz de confusión que resulta proviene de") 
  print("las clases reales del conjunto de prueba y de")
  print("las clases predichas del conjunto de prueba"+reset)
  print(rojo,matrizConfusion,reset)
  print(negro,"--------------------------------------------------------------------------------------------------------------------------------",reset)

# Generacion de matriz de confusion para cada clasificador
generarMConfusion(clasesRealesDPrueba, predichoNB)
generarMConfusion(clasesRealesDPrueba, predichoKNN)
generarMConfusion(clasesRealesDPrueba, predichoARB)

""">e) Anteriormente se muestró la matriz de confusión para cada clasificador utilizado, donde la misma se construye con las clase de pruba generadas con hold-out y con las clases predichas con cada clasificador puntual. Tmbién se puede ver que en los tres casos la diagonal de las matrices de confusión es la que tiene números mas altos, esto quiere decir que los clasificadores clasifican correctamente en su gran mayoría los ejemplos de estudio, esto se puede decir ya que en la diagonal principal de las matrices de confusión se encuentran los "casos" que son "verdaderos"; ej.: verdaderos positivos, verdaderos negatos, etc.

A continuació se mostrarán algunas métrica para compara los distintos clasicadores usados
"""

# Muestro distintas métricas
print(rojo, "Matriz de confusión para Naive-Bayes Multinomial: \n")
print(classification_report(clasesRealesDPrueba, predichoNB, target_names=clasesAux3),reset)

print(azul, "Matriz de confusión para Vecinos más cercanos(KNN): \n")
print(classification_report(clasesRealesDPrueba, predichoKNN, target_names=clasesAux3),reset)

print(verde, "Matriz de confusión para Árbol de decisión: \n")
print(classification_report(clasesRealesDPrueba, predichoARB, target_names=clasesAux3),reset)

"""A continuación se definieron varios tipos de validaciones cruzadas, las cuáles se aplicarán sobre los clasificadores vistos hasta el momento. Este procedimiento se realizó para obtenes varios resultados al particinar de maneras diferentes el dataset incial con el objetivo de generar una métrica promedio y su respectivo margen de error.

Se puede observa que para validación cruzada estandar y estratificada ambos con 5 particiones, la métrica observada es la misma, esto ocurre porque tanto los datos como las clases originales estan ordenadas, lo cual hace que las particiones sean las mismas.
"""

# Defino varios métodos de validacióin cruzada

cv_comun = 5                                             # común con 5 particones
cv_kfold = KFold(n_splits=5)
cv_strat = StratifiedKFold(n_splits=5)
cv_suffle = ShuffleSplit(n_splits=5)
cv_suffle_strat = StratifiedShuffleSplit(n_splits=5)

def obtenerScores(validacion, clasificador):
  print(negro+"---------------------------------------------------------------------------------------------------------------------------------------------------------"+reset)
  puntaje=cross_val_score(estimator=clasificador, X=datos, y=clasesAux ,cv=validacion)
  print(rojo+"Vector de puntajes(scores), con cv =",validacion,":",puntaje,reset)
  print(azul+"Se obtuvo una exactitud media de:","{0:.4f}".format(puntaje.mean()),", con un margen de error de +/-", "{0:.4f}".format(puntaje.std()*2)+reset)
  print(negro+"---------------------------------------------------------------------------------------------------------------------------------------------------------"+reset)

print(amarillo+"Se mostrará la métrica exactitud para sobre Naive-Bayes multinomial: "+reset)
obtenerScores(cv_comun, nbMultinomial)
obtenerScores(cv_strat, nbMultinomial)
obtenerScores(cv_suffle, nbMultinomial)
obtenerScores(cv_suffle_strat, nbMultinomial)

print(amarillo+"Se mostrará la métrica exactitud sobre Vecinos más cercanos (KNN): "+reset)
obtenerScores(cv_comun, vecinosMasCerca)
obtenerScores(cv_strat, vecinosMasCerca)
obtenerScores(cv_suffle, vecinosMasCerca)
obtenerScores(cv_suffle_strat, vecinosMasCerca)

print(amarillo+"Se mostrará la métrica exactitud sobre Árbol de decisión: "+reset)
obtenerScores(cv_comun, arbDecision)
obtenerScores(cv_strat, arbDecision)
obtenerScores(cv_suffle, arbDecision)
obtenerScores(cv_suffle_strat, arbDecision)

""">f) Debido a las características del dataset y los resultados obtenidos con nuestros clasificadores podemos afirmar que tienen aplicaciones interesantes. Una de ellas podría ser a futuro la creación de una aplicación que utilice al modelo para el reconocimiento de los distintos dígitos de los mapas daneses para la digitalización de los mismos. Esto es muy importante ya que preservaría una parte de la historia del país como información valiosa para éste. Además, al estar los números del dataset escritos a mano, también podría extenderse para la digitalización o el reconocimiento en otras áreas, como puede ser la estadística, matemática o cualquier otro ámbito donde los números destaquen.

Bibliografía:

* https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
* https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
* https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
* https://scikit-learn.org/0.16/modules/generated/sklearn.cross_validation.cross_val_score.html
* https://es.stackoverflow.com/questions/39726/python-conversi%C3%B3n-de-un-string-a-tipo-lista-sin-tener-los-caracteres-separados
* https://es.stackoverflow.com/questions/87813/eliminar-elementos-duplicados-en-una-lista
* https://www.programiz.com/python-programming/type-conversion-and-casting
* https://stackoverrun.com/es/q/264467
* https://es.wikipedia.org/wiki/%C3%81rbol_kd
"""