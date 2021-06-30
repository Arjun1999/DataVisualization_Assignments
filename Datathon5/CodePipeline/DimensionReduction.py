import numpy as np 
import pandas as pd
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import pyplot, patches
from sklearn.preprocessing import StandardScaler

# Reading the Dataset
df = pd.read_csv('Datathon4.csv')
df = df.query("Year == 2008")
T = df[['Country', 'Year', 'Total population', 'Population aged 64+, male', 'Population aged 64+, female',
        'Life expectancy at age 65, women', 'Life expectancy at age 65, men', 'GDP per capita at current prices and PPPs, US$',
        'Life expectancy at birth, women', 'Life expectancy at birth, men', 'Total fertility rate', 'Mean age of women at birth of first child',
        'Total employment, growth rate', 'Unemployment rate', 'Economic acivity rate, women 15-64', 'Economic activity rate, men 15-64',
        'Persons killed in road accidents', 'Total length of motorways (km)', 'Total length of railway lines (km)']]

# print(T.isnull().sum())
T.describe(include='all')



for col in T.columns.values:
    # print(col)
    if T[col].isnull().sum() == 0:

        continue
    else:
        guess_value = T[col].median()
        T[col].loc[(T[col].isnull())] = guess_value
# print(T.isnull().sum())
T.describe(include='all')


X = T[[ 'Total population', 'Population aged 64+, male', 'Population aged 64+, female',
        'Life expectancy at age 65, women', 'Life expectancy at age 65, men', 'GDP per capita at current prices and PPPs, US$',
        'Life expectancy at birth, women', 'Life expectancy at birth, men', 'Total fertility rate', 'Mean age of women at birth of first child',
        'Total employment, growth rate', 'Unemployment rate', 'Economic acivity rate, women 15-64', 'Economic activity rate, men 15-64',
        'Persons killed in road accidents', 'Total length of motorways (km)', 'Total length of railway lines (km)']]

# Creating Development Status
T['DevelopmentStatus'] = 'Developed'
T.loc[(T['GDP per capita at current prices and PPPs, US$'] < 25000), 'DevelopmentStatus'] = 'Developing'

X_scaled = StandardScaler().fit_transform(X)

# Visualizing original ordering 
new_X = X_scaled.dot(X_scaled.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_X,
              cmap = "inferno",
              interpolation="none", aspect='auto')
# pyplot.show()

# Computing Covariance Matrix
features = X_scaled.T
cov_matrix = np.cov(features)

# Computing Eigenvalues and Eigenvectors
values, vectors = np.linalg.eig(cov_matrix)

# Projecting onto first two principal components
projected_1 = X_scaled.dot(vectors.T[0])
projected_2 = X_scaled.dot(vectors.T[1])

# Soriting matrix according to projections
new_matrix1 = X_scaled[projected_1.argsort()]


# Visualizing Dataset along the top two projected components
plt.figure(figsize=(16, 12))
sns.scatterplot(projected_1, projected_2, hue=T['DevelopmentStatus'], s = 100)
plt.title('Dataset represtation for the sample year 2008 using PCs')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.show()


# Visualizing Re-ordered Matrix
new_X = new_matrix1.dot(new_matrix1.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_X,
              cmap = 'inferno',
              interpolation="none", aspect='auto')
# pyplot.show()
