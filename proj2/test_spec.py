import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import itertools
import pickle

#number of operations
op_count = 0

def max_clique_greedy(graph):
    if not graph.nodes:
        return []

    # Sort nodes by degree in descending order
    nodes_sorted_by_degree = sorted(graph.nodes, key=lambda x: graph.degree(x), reverse=True)

    # Initialize the clique with the first node
    clique_max = [nodes_sorted_by_degree[0]]

    for node in nodes_sorted_by_degree[1:]:
        if check_in_clique(node, clique_max, graph):
            clique_max.append(node)

    # Return the maximal clique
    return clique_max

def max_clique_greedy_alternative(graph):
    if not graph.nodes:
        return []

    clique_max = []
    
    for node in graph.nodes():
        aux_clique = [node]
        for n in graph.nodes():
            if n == node:
                continue
            else:
                if check_in_clique(n, aux_clique, graph):
                    aux_clique.append(n)
        
        if len(aux_clique) > len(clique_max):
            clique_max = aux_clique

    # Return the maximal clique
    return clique_max

def find_all_maximal_cliques(graph, size):
    # Use the Bron–Kerbosch algorithm to find all maximal cliques of a given size
    cliques = list(nx.find_cliques(graph))
    return [clique for clique in cliques if len(clique) == size]

def check_in_clique(node, clique_max, graph):
    global op_count
    neighbors = set(graph.neighbors(node))
    for n in clique_max:
        op_count += 1
        if n not in neighbors:
            return False
    return True


# MAIN

if len(sys.argv) < 2:
    print('ERROR! Usage: test.py <String : Graph file>', file=sys.stderr)
    sys.exit(1)

# CREATE GRAPH

file1 = open(sys.argv[1], 'r')
lines = file1.readlines()

if lines[0] == 1:
    is_oriented = True
else:
    is_oriented = False

if lines[0] == 1:
    has_weights = True
else:
    has_weights = False

G = nx.DiGraph() if is_oriented else nx.Graph()

for line in lines[4:]:
    edge_info = line.split()
    node1, node2 = int(edge_info[0]), int(edge_info[1])

    # Check if there is a weight specified
    if has_weights:
        weight = int(edge_info[2])
        G.add_edge(node1, node2, weight=weight)
    else:
        G.add_edge(node1, node2)

positions = {}
for node in G.nodes:
    positions[node] = (random.randint(0, 100), random.randint(0, 100))

max_clique_result = max_clique_greedy_alternative(G)

subgraph = nx.subgraph(G, max_clique_result)

plt.figure()
nx.draw(G, pos=positions, node_size=300, with_labels=True)
plt.title("Original Graph")

# Create the subgraph figure
plt.figure()
nx.draw(G, pos=positions, node_size=300, with_labels=True)
nx.draw(subgraph, pos=positions, edge_color = 'red',node_color='red', node_size=300, with_labels=True)
plt.title("Maximal Clique Subgraph")

# Find all maximal cliques with the same size as the maximum clique
all_maximal_cliques = find_all_maximal_cliques(G, len(max_clique_result))
print("Maximal Cliques with the Same Size:")
for clique in sorted(all_maximal_cliques):
    print(sorted(clique)) 


# Show the figures
plt.show()
