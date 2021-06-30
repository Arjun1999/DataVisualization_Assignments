#################################################################################################################################################################################
# For the purposes of implementation and testing, both the algorithms have been implemented on a somewhat easier (read cleaned and complete) dataset which is the IRIS Dataset" #
#################################################################################################################################################################################

import numpy as np
import pandas as pd
import scipy
from matplotlib import pyplot, patches
from sklearn.preprocessing import StandardScaler
# float_formatter = lambda x: "%.3f" % x
# np.set_printoptions(formatter={'float_kind':float_formatter})
# from sklearn.datasets.samples_generator import make_circles
from sklearn.metrics import pairwise_distances
from matplotlib import pyplot as plt
import networkx as nx
# import seaborn as sns
# sns.set()

# drawing a networkx graph
def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# Reading the Dataset
# df = pd.read_csv('https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv')
# df.head()

# X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

# For COVID
df = pd.read_csv('../Datathon4.csv')
X = df[['Population aged 64+, male', 'Population aged 64+, female', 'Life expectancy at age 65, women', 'Life expectancy at age 65, men']]

med1 = X['Population aged 64+, male'].median()
med2 = X['Population aged 64+, female'].median()
med3 = X['Life expectancy at age 65, women'].median()
med4 = X['Life expectancy at age 65, men'].median()

X['Population aged 64+, male'] = X['Population aged 64+, male'].fillna(med1)
X['Population aged 64+, female'] = X['Population aged 64+, male'].fillna(med2)
X['Life expectancy at age 65, women'] = X['Life expectancy at age 65, women'].fillna(med3)
X['Life expectancy at age 65, men'] = X['Life expectancy at age 65, men'].fillna(med4)

X_scaled = StandardScaler().fit_transform(X)

# print(X_scaled)
# Visualizing Original ordering
new_m = X_scaled.dot(X_scaled.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_m,
              cmap="inferno",
              interpolation="none", aspect='auto')
pyplot.show()

# Generating an adjacency matrix and the corresponding bipartite graph
W = pairwise_distances(X_scaled, metric="euclidean")
vectorizer = np.vectorize(lambda x: 1 if x < 0.3 else 0)
W = np.vectorize(vectorizer)(W)

# sparse matrix to visualize the bipartite graph
sparse_csr_mat = scipy.sparse.csr_matrix(W)
G = nx.algorithms.bipartite.matrix.from_biadjacency_matrix(sparse_csr_mat)
# draw_graph(G)

# degree matrix
D = np.diag(np.sum(np.array(W), axis=1))

# Laplacian Matrix
L = D - W

e, v = np.linalg.eig(L)  # eigenvalues
l = np.sort(e)


# Finding Fiedler Vector
sorted_value_vector = v[e.argsort()]
sorted_e = (np.sort(e))

# print(list(e))
# print(sorted_e)

for x in range(len(sorted_e)):
    if(sorted_e[x] > 0):
        # print(sorted_e[x])
        i = x
        break

# print(i)
# print(sorted_value_vector[i].shape)

projected_1 = sorted_value_vector[i]


# Sorting according to Fiedler Vector
sorted_fiedler_vector = X_scaled[projected_1.argsort()]

# Visualizing Re-ordered Matrix
new_m = sorted_fiedler_vector.dot(sorted_fiedler_vector.T)
fig = pyplot.figure(figsize=(10, 10))  # in inches
pyplot.imshow(new_m,
              cmap = 'inferno',
              interpolation="none", aspect = 'auto')
pyplot.show()
