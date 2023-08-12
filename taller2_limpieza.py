# -*- coding: utf-8 -*-
"""Taller2 Limpieza.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XVoVY9OkdW9-wBA4goBxWXF2s9vpTl7g
"""

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.stats import pearsonr, zscore

import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import linear_model

#Datos de propiedades
ruta = 'https://raw.githubusercontent.com/rasief/cartografia/master/melb_data.csv'
df = pd.read_csv(ruta)
df

df.dtypes

df = df.select_dtypes(exclude=['object'])
df

#Buscar nulos
df.isnull().sum()

#Borrado de datos nulos
df = df.dropna()
df

#Histograma
df.Price.hist(color='firebrick', bins=100, figsize=(10, 6))

#Diagrama de distribución
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(x = 'BuildingArea', y = 'Price', c = 'navy', kind = "scatter", ax = ax)
ax.set_title('Distribución de precio y area construida');

#Datos con área menor o igual a 800
df0 = df[df["BuildingArea"]<=800]
df0

#Diagrama de distribución
fig, ax = plt.subplots(figsize=(10, 6))
df0.plot(x = 'BuildingArea', y = 'Price', c = 'navy', kind = "scatter", ax = ax)
ax.set_title('Distribución de precio y area construida');

#Datos con área cero
dfzero = df0[df0["BuildingArea"]<5]
len(dfzero)

#Se eliminan los registros de menos de 15 mts cuadrados de area
df0 = df0[df0["BuildingArea"]>=5]
df0

#Se eliminan todos los datos que estén más allá de 3 desviaciones estándar
df0 = df0[(np.abs(zscore(df0['BuildingArea']))<=3)]
df0

#Boxplot
ax = sb.boxplot(data=df0['BuildingArea'].values, orient='h', color='yellow')
ax.set_title('Boxplot area construida');
plt.show()

#Múltiples diagramas por parejas
sb.set_theme(style="ticks")
sb.pairplot(df0, hue='Rooms')

#Correlación entre variables
corr_test = pearsonr(x = df['BuildingArea'], y = df['Price'])
print("Coeficiente de correlación de Pearson: ", corr_test[0])
print("P-value: ", corr_test[1])

colormap = plt.cm.viridis
plt.figure(figsize=(10, 10))
plt.title('Pearson Correlation of Features', y=1.05, size=15)
sb.heatmap(df.astype(float).corr(),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)

"""En la limpieza de Datos usaremos los valores de precio, Distancia respecto al centro, Rooms y Car que son datos que podemos relacionar directamente respecto al precio y que son principalmente relevantes al elegir una vivienda

No tendremos en cuenta el Area construida debido a que, Cuando las viviendas son apartamentos estos no pueden hacer remodelaciones o contrucciones fuera del area fijada por el edificio, Ya que al estar mas cerca al centro de la ciudad lo normal es encontrar más apartamentos que Casas.


Borraremos valores Nulos y graficaremos los anteriores valores para diferenciar los que tienen alta correlación y asi definir que queremos hacer con ellos.
"""

# Seleccionar las columnas de interés
selected_columns = ['Price', 'Distance', 'Rooms', 'Car']
selected_data = df[selected_columns]

# Eliminar los valores nulos
selected_data_cleaned = selected_data.dropna()

# Calcular la matriz de correlación de Pearson
correlation_matrix = selected_data_cleaned.corr()

# Configurar el mapa de colores
colormap = plt.cm.viridis

# Crear la figura
plt.figure(figsize=(10, 10))

# Título del gráfico
plt.title('Pearson Correlation of Features (Cleaned)', y=1.05, size=15)

# Crear el mapa de calor
sb.heatmap(correlation_matrix, linewidths=0.1, vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)

# Mostrar el gráfico
plt.show()

"""Por ejemplo, Podemos ver que la correlación mas alta que tenemos es la de Price evaluado en Rooms con un porcentaje de 0.52. Es decir que podemos decir que el precio de las viviendas esta casi relacionada al numero de cuartos individuales (No habitaciones necesariamente) de la vivienda. Estos 'Rooms' son Baños,Cocina,Sala, etc."""

selected_columns = ['Price', 'Rooms']
selected_data = df[selected_columns]

# Eliminar los valores nulos
selected_data_cleaned = selected_data.dropna()

# Crear el gráfico de combinación
plt.figure(figsize=(8, 6))
plt.scatter(selected_data_cleaned['Rooms'], selected_data_cleaned['Price'], alpha=0.5)
plt.title('Grafico de Combinación')
plt.xlabel('Rooms')
plt.ylabel('Price')
plt.grid(True)
plt.show()

"""Aqui usamos los valores de Price y Rooms en un grafico de Combinación para individualizar los datos de cada parte. Podemos ver como el precio en viviendas con cuartos de 3 a 5 no supera por mucho entre sí. Mientras que en viviendas con cuartos con 8 o más el precio no es distinto a estos"""