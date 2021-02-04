# -*- coding: utf-8 -*-
"""Entrega - IA - Regas de Asociacion - Andersson--Bertino-.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GFzH9mE_7ZgesnMklTOQtewokRnVxujg

TP - Reglas de Asociación

Integrantes: 
Andersson Erick, Bertino Ariel


a) El DataSet seleccionado("mushroom") consiste en más de 8100 entradas, donde cada una describe caracteristicas (23) de un tipo de hongo o seta determinado, pertenecientes a las familias Agaricus y Lepiota. Cada especie se identifica como comestible, venenosa, o de comestibilidad desconocida.

b) El objetivo de aplicar reglas de asociación es establecer elementos comunes entre elementos del DataSet con el objetivo de identificar patrones relevantes o de interés. El tipo de patrones que se espera encontrar en el DataSet serán en relaciones a cuán venenosos y comestibles son los hongos que el mismo contiene. Por otro lado se buscaría estables si dado alguna carracteristica esto implique la aparicion una o mas caracteristicas.
"""

""" TP2 - REGLAS DE ASOCIACIÓN """

# soporte para cargar dataset de https://www.openml.org/
!pip install openml
import numpy
import openml
import pandas as pd
from mlxtend import *
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

"""Acceso al dataset"""

# indicamos cual dataset queremos utilizar, en este caso el nro. 24
dataset = openml.datasets.get_dataset(24)

# separamos las información almacenada en el dataset
X, y, categorical_indicator, attribute_names = dataset.get_data(
    dataset_format='dataframe',
    target=dataset.default_target_attribute
)

#  concatenamos la información relevante en un único DataFrame 
df = pd.concat([X, y], axis=1)
df

"""d) Definir qué pre‐procesamiento se realizará a los datos. Justificar. Aplicarlo.

Preprocesamiento con getDummies()
"""

# Decidimos untilzar la funcion get_dummies() que nos brinda la 
# librería Pandas, esta funcion discretiza valores de el/los 
# campos requeridos, o de plano todos los campos. Cabe aclarar
# que la matriz resultante queda en formato, 'one hot encoded',
# formato requerido para posterior procesamiento

dfDummied = pd.get_dummies(df)
dfDummied

"""e) Obtener las reglas de asociación utilizando el dataset elegido. Definir parámetros del algoritmo. Justificar. 

Filtrado por valor mínimo de soporte
"""

""" Con soporte minimo de 0.5 se obtienen 2733 itemsets frecuentes
    Con soporte minimo de 0.5 se obtienen 153 itemsets frecuentes
    Con soporte minimo de 0.6 se obtienen 50 itemsets frecuentes
    Con soporte minimo de 0.7 se obtienen 30 itemsets frecuentes
    Con soporte minimo de 0.8 se obtienen 23 itemsets frecuentes        """

""" El parametro n_jobs asigna procesadores locales al computo del 
    algoritmo, -1, indica que se alsigne el maximo numero de
    procesadores disponibles de nuestra pc                              """

""" Por otro lado consideramos que seria mas útil solo incluir en el 
    analisis itemsets de temaño 3, esto lo indicamos con el parametro
    max_lenght=3, con lo cual, el resultado de correr el algoritmo
    arroja como resultado 20 itemsets mas frecuentes                    """

# Optamos por un soporte minimo de 0.8 ya que nos parecio mas representativo
# el numero de itemsets frecuentes encontrados, teniendo en cuenta que el
# soporte indica trasacciones en las cuales esos itemset se repiten

itemsetFrecuentes = apriori (dfDummiado, min_support=0.3, use_colnames=True, n_jobs=-1)
itemsetFrecuentes

"""Obtención de reglas de asociación a partir del itemset"""

""" Con el parametro metric, definimos bajo qué métrica queremos basar el resultado,
    a su vez con el parametro min_threshold establecemos el valor mínimo para esa
    métrica                                                                           """

# Basados en un valor de min_threshold = 0.8, con metrica support (soporte), se encuentran
# 59 reglas de asociacion, mientras que con confidence (confianza), se consiguen tambien
# 59 reglas.

reglasAsociacion = association_rules(itemsetFrecuentes, metric="confidence", min_threshold=0)
reglasAsociacion

"""f) Determinar qué post‐procesamiento se realizará sobre las reglas obtenidas. Aplicarlo.

Postprocesamiento de las reglas de asociación
"""

r1 = reglasAsociacion[reglasAsociacion['consequents'] == {'class_e'}]
r1[r1['support']>0.4].sort_values('support', ascending=False)

r2 = reglasAsociacion[reglasAsociacion['consequents'] == {'class_p'}]
r2[r2['support']>0.4].sort_values('support', ascending=False)

"""
g) Analizar las reglas de asociación obtenidas.

Las reglas de asociacion que pudimos obtener nos brindan un panorama general donde basados en ciertas caracteristicas presentes en un determinado hongo, poder determinar con un grado de soporte mayor al 40%, el dichoso hongo es comestible o venenoso. En el analisis no se tuvo en cuenta os hongos caranterizados como 'desconocidos', ya que al no tener mas datos discriminates sobre estos hongos no se pueden clasificar en comestibles o venenosos basados en caracteristicas previas.

h) Mostrar un ejemplo de cómo los resultados obtenidos pueden ser usados en el futuro.

Si bien en el dataset se explica que no hay una regla general que permita decir si un hongo es venenoso o comestible, se puede apreciar en las dos tablas de reglas de asociación presentadas anteriormente, para el caso de los hongos cuyo tipo de velo sea parcial pertenecen por lo general a la clase comestible, con un soporte y una confianza de 0.51.

A su vez, aquellos cuyo velo sea de color blanco, también pertenecen a la clase comestible con un soporte de 0,49 y una confianza de 0,5

Por otro lado, aquellos hongos cuyas branquias tengan un espaciado cercano son venenosos con un soporte de 0,46 y confianza de 0,55

Para concluir, cabe aclarar que para futuros datasets similares con caracteristicas de hongos se podrian llegar a detectar en el futuro si los hongos son venenoso o comestibles, por ejemplo en sitaciones de supervivencia o de campamento"""