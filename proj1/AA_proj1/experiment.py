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
                if check_in_clique(n,aux_clique,graph):
                    aux_clique.append(n)
        if len(aux_clique) > len(clique_max):
            clique_max = aux_clique

    # Return the maximal clique
    return clique_max

def check_in_clique(node,clique_max,graph):
    global op_count
    neighbors = set(graph.neighbors(node))
    for n in clique_max:
        op_count += 1
        if n not in neighbors:
            return False
    return True

# BRUTE-FORCE 
def max_clique_exhaustive(graph):
    if not graph.nodes:
        return []

    all_combinations = []

    for clique_size in range(2, len(graph.nodes) + 1):

        for nodes_combination in itertools.combinations(graph.nodes, clique_size):
            aux_clique = list(nodes_combination)
            all_combinations.append(aux_clique)

    max_clique = []

    for comb in all_combinations:

        if check_if_clique(comb,graph):
            if len(comb) > len(max_clique):
                max_clique = comb

    return max_clique

def check_if_clique(combination, graph):
    global op_count
    for n1 in combination:
        neighbors = set(graph.neighbors(n1))
        for n2 in combination:
            op_count += 1
            if n2 != n1 and n2 not in neighbors:
                return False
    return True


# MAIN

if len(sys.argv) < 2:
    print('ERROR! Usage: test.py <int : number of vertices> <float : percentage of edge creation>', file=sys.stderr)
    sys.exit(1)

if float(sys.argv[1]) <= 0 or float(sys.argv[1]) > 100:
    print('ERROR! percentage of edge creation must be ]0,100]', file=sys.stderr)
    sys.exit(1)

# initial number of nodes
n = 4

# number of experiments
e = 10

# percentage of edge creation
p = float(sys.argv[1]) / 100

# method
method = sys.argv[2]

list_medias = []
list_medias_op_count = []

# by nodes
while n < 26:

    l_time = []
    l_op_count = []
    print("\nNumber of nodes: "+str(n)+"\n")

    # by experiments
    for i in range(1, (e + 1)):
        op_count = 0
        # create random graph
        G = nx.fast_gnp_random_graph(n, p, 89356)

        # Create a dictionary of node positions between 0 and 100
        positions = {}
        for node in G.nodes:
            positions[node] = (random.randint(0, 100), random.randint(0, 100))

        start = time.time()

        if method == "e":
            max_clique_exhaustive(G)    
        elif method == "g":
            max_clique_greedy(G)
        elif method == "extra":
            max_clique_greedy_alternative(G)
        else:
            print('ERROR! Invalid algorithm! Available: <exhaustive> or <greedy>', file=sys.stderr)
            sys.exit(1)

        end = time.time()
        t = end - start
        l_time.append(t)
        print(f"Time {i}: %.8f" % t)
        l_op_count.append(op_count)
        print(op_count)

    media_time = sum(l_time) / e
    list_medias.append(media_time)

    media_op_count = sum(l_op_count) / e
    list_medias_op_count.append(media_op_count)

    n += 1

# MAKE PLOTS
# Plot 1: Average Time vs. Number of Nodes
plt.subplot(2, 1, 1)
x_values = list(range(4, n))
y_values = list_medias
plt.scatter(x_values, y_values, label='Experiment Time', s=10)
plt.plot(x_values, y_values, linestyle='-', marker='', color='gray', alpha=0.5)
plt.xlabel('Number of Nodes')
plt.ylabel('Average Time')

if method == "e":
    plt.title('Exhaustive - ' + str(float(sys.argv[1])) + '%')
    #plt.savefig('medium_times_exhaustive_' + str(float(sys.argv[1])) + '.png')
elif method == "g":
    plt.title('Greedy - ' + str(float(sys.argv[1])) + '%')
    #plt.savefig('medium_times_greedy_' + str(float(sys.argv[1])) + '.png')

# Plot 2: Number of Op_Count vs. Number of Nodes
plt.subplot(2, 1, 2)
y_values_op_count = list_medias_op_count
plt.scatter(x_values, y_values_op_count, label='Op_Count', s=10)
plt.plot(x_values, y_values_op_count, linestyle='-', marker='', color='red', alpha=0.5)
plt.xlabel('Number of Nodes')
plt.ylabel('Average Op_Count')

# Show the plots
plt.tight_layout()
plt.legend()
plt.show()