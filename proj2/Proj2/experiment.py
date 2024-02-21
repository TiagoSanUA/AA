import sys
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import itertools
from tabulate import tabulate

#number of operations
op_count = 0

# Check is set of nodes form a clique
def is_clique(graph, nodes):
    global op_count
    for pair in itertools.combinations(nodes, 2):
        op_count += 1
        if pair[1] not in graph[pair[0]]:
            return False
    return True

# Randomized algorithm to find max clique
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

# Create random graph with specific info from argv
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

# Create graph from txt file
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

if len(sys.argv) < 2:
    print('ERROR! Usage: experiment.py <int : number of vertices> <float : percentage of edge creation>', file=sys.stderr)
    print('       OR experiment.py filename.txt')
    sys.exit(1)

n_tries = 0

############ CREATE GRAPH ############

aux = sys.argv[1]

if aux.isdigit():
    G = create_from_argv()

elif (isinstance(aux,str)):
    G = create_from_file()
    
else:
    print('EROOR! Invalid arguments', file=sys.stderr)
    sys.exit(1)

# Create a dictionary of node positions between 0 and 100
positions = {}
for node in G.nodes:
    positions[node] = (random.randint(0, 100), random.randint(0, 100))

n_tries = 0.01  # Start with 1%

end_tries = 0.91  # Go up to 90%
increment_percentage = 0.1  # Increment by 10%

list_medias = []
list_medias_op_count = []
success_percentages = []

e = 10

x_values = []  # Initialize an empty list for x-axis values

while n_tries <= end_tries:
    num_tries = math.ceil(len(G.nodes) * n_tries)
    x_values.append(int(n_tries * 100))  # Convert the percentage to a whole number
    print("\nNumber of tries: ", num_tries)
    n_success = 0
    l_time = []
    l_op_count = []

    for i in range(e):
        op_count = 0
        start = time.time()
        max_clique_result = randomized_max_clique(G, num_tries)
        print("Max Clique:", max_clique_result)

        end = time.time()
        t = end - start
        l_time.append(t)

        print(f"Time {i}: %.8f" % t)

        print(op_count)
        l_op_count.append(op_count)

    media_time = sum(l_time) / e
    list_medias.append(media_time)

    media_op_count = sum(l_op_count) / e
    list_medias_op_count.append(media_op_count)

    n_tries += increment_percentage


# MAKE PLOTS
# Plot 1: Average Time vs. Number of Tries
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
y_values = list_medias
plt.scatter(x_values, y_values, label='Experiment Time', s=10, color='blue')
plt.plot(x_values, y_values, linestyle='-', marker='', color='blue', alpha=0.5)
plt.xlabel('Number of Tries')
plt.ylabel('Average Time')
plt.title('Randomized Algorithm - Average Time vs. Number of Tries')

# Plot 2: Number of Op_Count vs. Number of Tries
plt.subplot(2, 1, 2)
y_values_op_count = list_medias_op_count
plt.scatter(x_values, y_values_op_count, label='Op_Count', s=10, color='red')
plt.plot(x_values, y_values_op_count, linestyle='-', marker='', color='red', alpha=0.5)
plt.xlabel('Number of Tries')
plt.ylabel('Average Op_Count')
plt.title('Randomized Algorithm - Average Op_Count vs. Number of Tries')

# Show the plots
plt.tight_layout()
plt.legend()
plt.show()