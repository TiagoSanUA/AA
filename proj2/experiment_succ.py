import sys
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
from tabulate import tabulate

# number of operations
op_count = 0

# Check if a set of nodes form a clique
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

# Greedy way to find max clique (used to determine success rate)
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

# Given a max clique find all others with the same size
def find_all_maximal_cliques(graph, size):
    # Use the Bron–Kerbosch algorithm to find all maximal cliques of a given size
    cliques = list(nx.find_cliques(graph))
    return [clique for clique in cliques if len(clique) == size]

# Check if node is in current max clique
def check_in_clique(node, clique_max, graph):
    global op_count
    neighbors = set(graph.neighbors(node))
    for n in clique_max:
        op_count += 1
        if n not in neighbors:
            return False
    return True

# Create random graph with specific info from argv
def create_from_argv():
    n = int(sys.argv[1])

    if float(sys.argv[2]) <= 0 or float(sys.argv[2]) > 100:
        print('ERROR! percentage of edge creation must be in the range (0, 100]', file=sys.stderr)
        sys.exit(1)

    # number edges
    p = float(sys.argv[2]) / 100

    # create random graph
    G = nx.fast_gnp_random_graph(n, p, 89356)

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

n_tries = 0.01  # Start with 1%

end_tries = 0.91  # Go up to 90%
increment_percentage = 0.1  # Increment by 5%

e = 10  # Number of iterations

success_percentages_all = []

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

for _ in range(3):  # Repeat the process 3 times

    max_clique_result = max_clique_greedy_alternative(G)
    all_maximal_cliques = find_all_maximal_cliques(G, len(max_clique_result))

    x_values = []  # Initialize an empty list for x-axis values
    success_percentages = []

    n_tries = 0.01  # Reset n_tries for each iteration

    while n_tries <= end_tries:
        num_tries = math.ceil(len(G.nodes) * n_tries)
        print("\nNumber of tries: ", num_tries)
        n_success = 0
        for i in range(e):
            max_clique_result = randomized_max_clique(G, num_tries)
            print("Max Clique:", max_clique_result)
            if set(max_clique_result) in map(set, all_maximal_cliques):
                n_success += 1
                print("Success!")

        success_percentage = (n_success / e) * 100
        success_percentages.append(success_percentage)

        n_tries += increment_percentage
        x_values.append(int(num_tries))

    success_percentages_all.append(success_percentages)

# Calculate the average success percentages
average_percentages = [sum(x) / len(x) for x in zip(*success_percentages_all)]

# Display the results in a table
table_data = list(zip(x_values, *success_percentages_all, average_percentages))
table_headers = ["Number of Tries", "Success Percentage (Run 1)", "Success Percentage (Run 2)", "Success Percentage (Run 3)", "Average Success Percentage"]
table = tabulate(table_data, headers=table_headers, tablefmt="pretty")
print("\nSuccess Percentage Table:")
print(table)
