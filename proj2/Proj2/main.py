import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import itertools

#number of operations
op_count = 0

def is_clique(graph, nodes):
    global op_count
    for pair in itertools.combinations(nodes, 2):
        op_count += 1
        if pair[1] not in graph[pair[0]]:
            return False
    return True

def randomized_max_clique(graph, num_tries):
    global op_count
    max_clique = set()

    for _ in range(num_tries):
        # Randomly permute the vertices of the graph
        vertices = list(graph.nodes)
        random.shuffle(vertices)

        # Attempt to form a clique starting from the randomly chosen node
        current_clique = set()
        for v in vertices:
            op_count += 1

            # Add v to clique if adjacent to all vertices in the current clique
            if is_clique(graph, current_clique | {v}):
                current_clique.add(v)

        # Check if the current clique is larger than the previously found maximum clique
        if len(current_clique) > len(max_clique):
            max_clique = current_clique.copy()

    return max_clique

def create_from_argv():
    n = int(sys.argv[1])

    if float(sys.argv[2]) <= 0 or float(sys.argv[2]) > 100:
        print('EROOR! percentage of egde creation must be ]0,100]', file=sys.stderr)
        sys.exit(1)

    # number edges
    p = float(sys.argv[2])/100

    # create random graph
    G = nx.fast_gnp_random_graph(n,p,89356)

    return G

    
def create_from_file():
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
    
    return G

# MAIN

if len(sys.argv) < 3:
    print('ERROR! Usage: test.py <int : number of vertices> <float : percentage of edge creation> <int | number of tries>', file=sys.stderr)
    print('       OR test.py SW_ALGUNS_GRAFOS/filename.txt <int | number of tries>')
    sys.exit(1)

############ CREATE GRAPH ############

n_tries = 0

aux = sys.argv[1]

if aux.isdigit():
    G = create_from_argv()
    n_tries = int(sys.argv[3])

elif (isinstance(sys.argv[1],str)):
    G = create_from_file
    n_tries = int(sys.argv[2])

else:
    print('EROOR! Invalid arguments', file=sys.stderr)
    sys.exit(1)

# Create a dictionary of node positions between 0 and 100
positions = {}
for node in G.nodes:
    positions[node] = (random.randint(0, 100), random.randint(0, 100))

max_clique_result = randomized_max_clique(G,n_tries)
print("Max Clique:", max_clique_result)

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
