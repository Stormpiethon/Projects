# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Graph creation and visualization using NetworkX
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import networkx as nx
import matplotlib.pyplot as plt

# import the deque library
from collections import deque

# Import the heapq library
import heapq

# *******************************************************************************************
# Breadth-First Search (BFS)
def bfs(graph, start_node):
    # Keep track of the visited nodes
    visited = set()
    # Use a queue to perform BFS
    queue = deque([start_node])
    # Store the oder of traversal
    traversal_order = []

    while queue:
        # Pop the first node from the queue
        node = queue.popleft()

        # If the node has not been visited
        if node not in visited:
            # Mark the node as visited
            visited.add(node)
            # Add the node to the traversal order
            traversal_order.append(node)
            # Add the neighbors of the node to the queue
            queue.extend(graph.neighbors(node))

    return traversal_order

# *******************************************************************************************
# Depth-First Search (DFS)
def dfs(graph, start_node, visited=None):
    if visited is None:
        # Keep track of visited nodes
        visited = set()

    # Add the start node to the visited set
    visited.add(start_node)
    # Store the order of traversal
    traversal_order = [start_node]

    # Recursively visit the neighbors of the current node
    for neighbor in graph.neighbors(start_node):
        if neighbor not in visited:
            # Recursively visit neighbors
            traversal_order.extend(dfs(graph, neighbor, visited))

    return traversal_order

# *******************************************************************************************
# Dijkstra's Algorithm
def dijkstra(graph, start_node):
    # Priority queue to store (distance, node)
    pq = [(0, start_node)]
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0

    # Keep track of the visited nodes
    visited = set()
    
    # Loop until the priority queue is empty
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Skip if we've already processed this node
        if current_node in visited:
            continue
        
        # Mark the node as visited
        visited.add(current_node)
        
        # Update distances for neighbors
        for neighbor, attributes in graph[current_node].items():
            weight = attributes['weight']
            distance = current_distance + weight
            
            # If the new distance is shorter, update it
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Add the neighbor to the priority queue
                heapq.heappush(pq, (distance, neighbor))
    
    return distances

# *******************************************************************************************

# Create an empty graph
G = nx.DiGraph()

# Add vertices (nodes)
G.add_nodes_from([
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'
    ])

# Add edges (connections between nodes)
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'),
    ('C', 'F'), ('D', 'G'), ('E', 'H'), ('F', 'I'),
    ('G', 'J'), ('H', 'K'), ('I', 'L'), ('J', 'M'),
    ('K', 'N'), ('L', 'O'), ('M', 'P'), ('N', 'Q'),
    ('O', 'R'), ('P', 'S'), ('Q', 'T')
])

# Create a new graph for Dijkstra's algorithm
W = nx.Graph()

# Add nodes to the graph for Dijktra's algorithm
W.add_nodes_from([
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'
    ])

# Define a weighted graph with random weights
weighted_edges = [
    ('A', 'B', 9), ('A', 'C', 10), ('B', 'D', 6), ('B', 'E', 8),
    ('C', 'F', 10), ('D', 'G', 3), ('E', 'H', 9), ('F', 'I', 5),
    ('G', 'J', 8), ('H', 'K', 6), ('I', 'L', 4), ('J', 'M', 4),
    ('K', 'N', 10), ('L', 'O', 5), ('M', 'P', 10), ('N', 'Q', 1),
    ('O', 'R', 9), ('P', 'S', 8), ('Q', 'T', 7)
]


# Add weighted edges to the graph
W.add_weighted_edges_from(weighted_edges)

# Print nodes and edges
print("Nodes:", G.nodes())
print("Edges:", G.edges())

# Perform BFS on the new graph
bfs_result = bfs(G, start_node='A')
print("\nBFS Traversal:", bfs_result)

# Perform DFS on the new graph
dfs_result = dfs(G, start_node='A')
print("DFS Traversal:", dfs_result)

# Run Dijkstra's Algorithm from node 'A'
shortest_paths = dijkstra(W, start_node='A')
print("Shortest paths from 'A':", shortest_paths)

# Visualize the graph
nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold')
plt.show()

# Visualize the weighted graph
pos = nx.spring_layout(W)
nx.draw(W, pos, with_labels=True, node_color='lightblue', font_weight='bold')
edge_labels = nx.get_edge_attributes(W, 'weight')
nx.draw_networkx_edge_labels(W, pos, edge_labels=edge_labels)
plt.show()

adj_matrix = nx.adjacency_matrix(G)
adj_list = nx.to_dict_of_lists(G)
edge_list = nx.to_edgelist(G)

# Display the adjacency matrix
print("\nAdjacency Matrix:")
print(adj_matrix.toarray())

# Display the adjacency list
print("\nAdjacency List:")
for node, neighbors in adj_list.items():
    print(f"{node}: {neighbors}")

# Display the edge list
print("\nEdge List:")
for edge in edge_list:
    print(edge)