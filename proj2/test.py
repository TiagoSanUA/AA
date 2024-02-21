import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import itertools

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
if len(sys.argv) < 3:
    print('ERROR! Usage: test.py <int : number of vertices> <float : percentage of edge creation>', file=sys.stderr)
    sys.exit(1)

if float(sys.argv[2]) <= 0 or float(sys.argv[2]) > 100:
    print('EROOR! percentage of egde creation must be ]0,100]', file=sys.stderr)
    sys.exit(1)

# number nodes
n = int(sys.argv[1])

# number edges
p = float(sys.argv[2])/100

# create random graph
G = nx.fast_gnp_random_graph(n,p,89356)

# Create a dictionary of node positions between 0 and 100
positions = {}
for node in G.nodes:
    positions[node] = (random.randint(0, 100), random.randint(0, 100))

start = time.time()

max_clique_result = max_clique_greedy(G)
print("Max Clique:", max_clique_result)

end = time.time()
t = end - start
print("Time: %.5f" % t)

print(op_count)

subgraph = nx.subgraph(G, max_clique_result)

plt.figure()
nx.draw(G, pos=positions, node_size=300, with_labels=True)
plt.title("Original Graph")

# Create the subgraph figure
plt.figure()
nx.draw(G, pos=positions, node_size=300, with_labels=True)
nx.draw(subgraph, pos=positions, edge_color = 'red',node_color='red', node_size=300, with_labels=True)
plt.title("Maximal Clique Subgraph")

# Show the figures
plt.show()