# -*- coding: utf-8 -*-
"""Práctica5Patrones.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i6re58Rc-PNQMxV0aRKJ5VTm6wgfsKKE
"""

import numpy as np

help(np.random.rayleigh)

#1. Generar una muestra aleatoria de 10, 000 puntos de la distribuci ́on de Rayleigh utilizando scale = 7.53
scale = 7.53
N = 10000
#Obtén 160 puntos del histograma de tu muestra.
nbins = 160

rayleigh_data = np.random.rayleigh(scale=scale, size=N)

rayleigh_data

import matplotlib.pyplot as plt

# Muestra aleatoria
plt.plot(rayleigh_data)

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
#3.Divide los puntos en conjunto de entrenamiento y prueba (80-20).
train_data, test_data = train_test_split(rayleigh_data, test_size=0.2, random_state=42)

#4. Realiza una regresi ́on polinomial del conjunto de entrenamiento probando distintos grados
# de polinomio. Calcula el sesgo y varianza para cada grado utilizado (Es posible que
# tengas que dividir tu conjunto de entrenamiento en entrenamiento y validaci ́on). Imprime
# los resultados en un dataframe de pandas: grado del polinomio, sesgo, varianza, MAE, MSE, R2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Creación de DataFrame
results_df = pd.DataFrame(columns=['Grado del Polinomio', 'Sesgo', 'Varianza', 'MAE', 'MSE', 'R2'])

# Rango de grados del polinomio
grados_polinomio = [1, 2, 3, 7, 10]

# División del conjunto en entrenamiento y validación
X_entrenamiento, X_validacion, y_entrenamiento, y_validacion = train_test_split(train_data.reshape(-1, 1),train_data,test_size=0.2,random_state=42)

for grado in grados_polinomio:
    polynomial_features = PolynomialFeatures(degree=grado)
    X_poly_train = polynomial_features.fit_transform(X_entrenamiento)
    X_poly_val = polynomial_features.transform(X_validacion)

    # Entrenamos el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_poly_train, y_entrenamiento)

    # Predicciones en el conjunto de validación
    y_predicciones_validacion = model.predict(X_poly_val)

    mae = mean_absolute_error(y_validacion, y_predicciones_validacion)
    mse = mean_squared_error(y_validacion, y_predicciones_validacion)
    r2 = r2_score(y_validacion, y_predicciones_validacion)

    # Calculos de sesgo y varianza
    sesgo = np.mean((y_predicciones_validacion - y_validacion.mean()) ** 2)
    varianza = np.var(y_predicciones_validacion)

    results_df = pd.concat([results_df, pd.DataFrame({'Grado del Polinomio': [grado],'Sesgo': [sesgo],'Varianza': [varianza],'MAE': [mae],'MSE': [mse],'R2': [r2]})], ignore_index=True)

print(results_df)

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge, Lasso
from sklearn.pipeline import make_pipeline

# Crear DataFrame para almacenar los resultados
results_df = pd.DataFrame(columns=['Grado del Polinomio', 'Tipo de Regularización', 'MAE', 'MSE', 'R2'])

# Definir el rango de grados del polinomio a probar
grados_polinomio = [1, 2, 3, 4, 5, 7, 10]

# Dividir el conjunto de entrenamiento en entrenamiento y validación
X_entrenamiento, X_validacion, y_entrenamiento, y_validacion = train_test_split(train_data.reshape(-1, 1),
                                                  train_data,
                                                  test_size=0.2,
                                                  random_state=42)

for grado in grados_polinomio:
    for regularizacion in ['Lasso', 'Ridge']:
        # Crear el modelo de regresión polinomial con regularización
        if regularizacion == 'Lasso':
            model = make_pipeline(PolynomialFeatures(degree=grado), StandardScaler(), Lasso(alpha=0.01))
        else:
            model = make_pipeline(PolynomialFeatures(degree=grado), StandardScaler(), Ridge(alpha=0.01))

        # Calcular puntuaciones de validación cruzada
        scores_mae = -cross_val_score(model, X_entrenamiento, y_entrenamiento, scoring='neg_mean_absolute_error', cv=5)
        scores_mse = -cross_val_score(model, X_entrenamiento, y_entrenamiento, scoring='neg_mean_squared_error', cv=5)
        scores_r2 = cross_val_score(model, X_entrenamiento, y_entrenamiento, scoring='r2', cv=5)

        # Guardar resultados en el DataFrame
        results_df = pd.concat([results_df, pd.DataFrame({'Grado del Polinomio': [grado],
                                                          'Tipo de Regularización': [regularizacion],
                                                          'MAE': [np.mean(scores_mae)],
                                                          'MSE': [np.mean(scores_mse)],
                                                          'R2': [np.mean(scores_r2)]})], ignore_index=True)

print(results_df)

#Encontrar el modelo con el puntaje R2 más alto:
mejor_modelo = results_df.loc[results_df['R2'].idxmax()]
print("Mejor modelo polinomial:")
print(mejor_modelo)

# Estimar el parámetro de escala (MLE)
scale_MLE = np.sqrt(np.mean(train_data ** 2) / 2)

# Generar muestras de la distribución de Rayleigh utilizando el parámetro de escala estimado
rayleigh_data_MLE = np.random.rayleigh(scale=scale_MLE, size=len(test_data))

# Calcular métricas de evaluación para el modelo de Rayleigh MLE en el conjunto de prueba
MAE_MLE = mean_absolute_error(test_data, rayleigh_data_MLE)
MSE_MLE = mean_squared_error(test_data, rayleigh_data_MLE)
R2_MLE = r2_score(test_data, rayleigh_data_MLE)

# Mostrar resultados
print("Rendimiento del modelo de Rayleigh MLE en el conjunto de prueba:")
print("MAE:", MAE_MLE)
print("MSE:", MSE_MLE)
print("R2:", R2_MLE)

# Comparar con el rendimiento del modelo polinomial
print("\nRendimiento del modelo polinomial en el conjunto de prueba:")
print("MAE:", best_model['MAE'])
print("MSE:", best_model['MSE'])
print("R2:", best_model['R2'])