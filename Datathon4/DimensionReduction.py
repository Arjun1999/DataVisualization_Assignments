#################################################################################################################################################################################
# For the purposes of implementation and testing, both the algorithms have been implemented on a somewhat easier (read cleaned and complete) dataset which is the IRIS Dataset" #
#################################################################################################################################################################################
import numpy as np 
import pandas as pd
import networkx as nx
from matplotlib import pyplot, patches
from sklearn.preprocessing import StandardScaler

# Reading the Dataset
df = pd.read_csv('https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv')
df.head()
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

# For COVID
# df = pd.read_csv('../Datathon4.csv')
# X = df[['Population aged 64+, male', 'Population aged 64+, female', 'Life expectancy at age 65, women', 'Life expectancy at age 65, men']]

# med1 = X['Population aged 64+, male'].median()
# med2 = X['Population aged 64+, female'].median()
# med3 = X['Life expectancy at age 65, women'].median()
# med4 = X['Life expectancy at age 65, men'].median()

# X['Population aged 64+, male'] = X['Population aged 64+, male'].fillna(med1)
# X['Population aged 64+, female'] = X['Population aged 64+, male'].fillna(med2)
# X['Life expectancy at age 65, women'] = X['Life expectancy at age 65, women'].fillna(med3)
# X['Life expectancy at age 65, men'] = X['Life expectancy at age 65, men'].fillna(med4)

# print(X)
X_scaled = StandardScaler().fit_transform(X)

# Visualizing original ordering 
new_X = X_scaled.dot(X_scaled.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_X,
              cmap = "inferno",
              interpolation="none", aspect='auto')
pyplot.show()

# Computing Covariance Matrix
features = X_scaled.T
cov_matrix = np.cov(features)

# Computing Eigenvalues and Eigenvectors
values, vectors = np.linalg.eig(cov_matrix)

# Projecting onto first principal component
projected_1 = X_scaled.dot(vectors.T[0])

# Soriting matrix according to projections
new_matrix1 = X_scaled[projected_1.argsort()]

# Visualizing Re-ordered Matrix
new_X = new_matrix1.dot(new_matrix1.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_X,
              cmap = 'inferno',
              interpolation="none", aspect='auto')
pyplot.show()
