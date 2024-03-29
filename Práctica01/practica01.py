# -*- coding: utf-8 -*-
"""Practica01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KLZpG4ffjcjVHKdldNDU8xxQY03efe54
"""

# Leer el csv de horas_dedicadas
import pandas as pd #Importamos pandas

df_datos = pd.read_csv("datos.csv")
df_datos



#Quitar valores nulos .fillna()
df_final= df_datos["calificaciones_obtenida"].fillna(0)
df_final

import numpy as np

"""**DATOS DE LAS HORAS**"""

# Obtener la media del número de horas
df_datos["horas_dedicadas"].mean()

# Obtener las hora más alta
df_datos["horas_dedicadas"].max()

# Obtener la hora más baja
df_datos["horas_dedicadas"].min()

# Desviación estándar de horas dedicadas
desviacion_estandar_horas = df_datos["horas_dedicadas"].std()
desviacion_estandar_horas

"""**DATOS DE LAS CALIFICACIONES**

"""

# Obtener la media de las calificaciones obtenida
df_final.mean()

# Obtener la calificacion mas alta
df_final.max()

# Obtener la calificación mas pequeña
df_final.min()

# Desviación estándar de calificaciones obtenidas
desviacion_estandar_calificaciones = df_final.std()
desviacion_estandar_calificaciones

"""**MODELO DE REGRESIÓN**"""

from sklearn.linear_model import LinearRegression

# obtener la lista de horas y de calificaciones, el de calificaciones convertirlo a array de numpy
horas = np.array(df_datos["horas_dedicadas"])
print(horas)
calificaciones = np.array(df_final)
calificaciones

#Aplicar reshape() al array de horas para transponerlo
horas = horas.reshape(-1,1)
horas

# Crear el modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo con los datos
modelo.fit(horas,calificaciones) #Fit entrena
# Predecir la calificacón de un estudiante
#317207488 3+1+7+2+0+7+4+8+8%50 -> 40%50
modelo.predict(np.array([[40]]))

import matplotlib.pyplot as plt

# Graficar los datos y la línea de regresión
plt.scatter(horas, calificaciones, color='green')
plt.plot(horas, modelo.predict(horas), color='yellow')
plt.title('Regresión Lineal: Horas Dedicadas vs Calificación Obtenida')
plt.xlabel('Horas Dedicadas')
plt.ylabel('Calificación Obtenida')
plt.show()