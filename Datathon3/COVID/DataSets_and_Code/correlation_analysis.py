#################################################################################################################################
# Note : This code was taken as is from a TDS article just to check the usability of correlations for the problem statement being explored.
# Unfortunately, it wasn't much helpful and was thus left as is.
# This can be ignored for the purposes of this datathon.
# This was just included to show that various approaches were explored however were consciously chosen to be omitted.
#################################################################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


# FinalCorrelations.csv is again another csv that was seperately worked upon to capture as much relevant data as possible 
# from COVID19_open_line_list.csv using another script. This however as mentined earlier did not prove to be as useful as it was expected to be.


#reads the csv
df = pd.read_csv('FinalCorrelationNew.csv') # To build a network based on the correlationf of attributes in the csv.

#creates a correlation matrix
cor_matrix = df.iloc[:, 1:].corr()

#shows the first 5 rows
print(cor_matrix.head())

#extracts the indices from the correlation matrix
attributes = cor_matrix.index.values

#Changes from dataframe to matrix, so it is easier to create a graph with networkx
cor_matrix = np.asmatrix(cor_matrix)

#Creates graph using the data of the correlation matrix
G = nx.from_numpy_matrix(cor_matrix)

#relabels the nodes to match the  attributes names
G = nx.relabel_nodes(G, lambda x: attributes[x])

#shows the edges with their corresponding weights
G.edges(data=True)

#function to create and display networks from the correlatin matrix.


def create_corr_network_1(G):
    #crates a list for edges and for the weights
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

    #positions
    positions = nx.circular_layout(G)

    #Figure size
    plt.figure(figsize=(15, 15))

    #draws nodes
    nx.draw_networkx_nodes(G, positions, node_color='#DA70D6',
                           node_size=500, alpha=0.8)

    #Styling for labels
    nx.draw_networkx_labels(G, positions, font_size=8,
                            font_family='sans-serif')

    #draws the edges
    nx.draw_networkx_edges(G, positions, edge_list=edges, style='solid')

    # displays the graph without axis
    plt.axis('off')
    #saves image
    plt.savefig("part1.png", format="PNG")
    plt.show()


create_corr_network_1(G)


def create_corr_network(G, corr_direction):

    ##Creates a copy of the graph
    H = G.copy()

    ##Checks all the edges and removes some based on corr_direction
    for attribute1, attribute2, weight in G.edges_iter(data=True):
        ##if we only want to see the positive correlations we then delete the edges with weight smaller than 0
        if corr_direction == "positive":
            if weight["weight"] < 0:
                H.remove_edge(attribute1, attribute2)
        ##this part runs if the corr_direction is negative and removes edges with weights equal or largen than 0
        else:
            if weight["weight"] >= 0:
                H.remove_edge(attribute1, attribute2)

### increases the value of weights, so that they are more visible in the graph
weights = tuple([(1+abs(x))**2 for x in weights])

###edge colors based on weight direction
if corr_direction == "positive":
    edge_colour = plt.cm.GnBu 
else:
    edge_colour = plt.cm.PuRd

#draws the edges
nx.draw_networkx_edges(H, positions, edge_list=edges,style='solid',
                      ###adds width=weights and edge_color = weights 
                      ###so that edges are based on the weight parameter 
                      ###edge_cmap is for the color scale based on the weight
                      ### edge_vmin and edge_vmax assign the min and max weights for the width
                      width=weights, edge_color = weights, edge_cmap = edge_colour,
                      edge_vmin = min(weights), edge_vmax=max(weights))

def create_corr_network(G, corr_direction, min_correlation):

##Checks all the edges and removes some based on corr_direction
for attribute1, attribute2, weight in G.edges_iter(data=True):
    ##if we only want to see the positive correlations we then delete the edges with weight smaller than 0        
    if corr_direction == "positive":
        ####it adds a minimum value for correlation. 
        ####If correlation weaker than the min, then it deletes the edge
        if weight["weight"] <0 or weight["weight"] < min_correlation:
            H.remove_edge(attribute1, attribute2)
    ##this part runs if the corr_direction is negative and removes edges with weights equal or largen than 0
    else:
        ####it adds a minimum value for correlation. 
        ####If correlation weaker than the min, then it deletes the edge
        if weight["weight"] >=0 or weight["weight"] > min_correlation:
            H.remove_edge(attribute1, attribute2)

#####calculates the degree of each node
d = nx.degree(H)
#####creates list of nodes and a list their degrees that will be used later for their sizes
nodelist, node_sizes = zip(*d.items())

#draws nodes
nx.draw_networkx_nodes(H,positions,node_color='#DA70D6',nodelist=nodelist,
                       #####the node size will be now based on its degree
                       node_size=tuple([x**3 for x in node_sizes]),alpha=0.8)
