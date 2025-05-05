import csv  # Module to handle CSV file reading
import heapq  # Module for priority queue (min-heap) operations
from collections import defaultdict  # Module to create a default dictionary for the graph

# Function to import a graph from a CSV file
def import_graph(fileman):
    # Create an adjacency list representation of the graph
    graph = defaultdict(list)
    with open(fileman, "r") as file:
        reader = csv.DictReader(file)  # Read each row as a dictionary using column headers
        for row in reader:
            src = row["source"]         # Get the source node from the row
            tgt = row["target"]         # Get the target node from the row
            weight = int(row["weight"]) # Convert the weight to an integer
            graph[src].append((tgt, weight))  # Add the edge (target, weight) to the source's list
    return graph  # Return the completed graph

# Function to perform Dijkstra's algorithm to find the shortest path between two nodes
def dijkstra(graph, start, end):
    # Initialize distances to all nodes as infinity, except the start node (set to 0)
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    # Initialize a dictionary to keep track of the previous node for each node (used to reconstruct path)
    pNode = {node: None for node in graph}

    # Create a priority queue (min-heap) to store (distance, node) pairs
    queue = [(0, start)]

    while queue:
        # Pop the node with the smallest current distance
        currentD, currentN = heapq.heappop(queue)

        # If we reached the end node, we can stop early
        if currentN == end:
            break

        # Check all neighbors of the current node
        for neighbor, weight in graph[currentN]:
            distance = currentD + weight  # Calculate the new distance
            # If the new distance is shorter, update the distance and previous node
            if distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = distance
                pNode[neighbor] = currentN
                heapq.heappush(queue, (distance, neighbor))  # Push the updated distance to the queue

    # Reconstruct the shortest path by tracing back from the end node
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = pNode.get(current)
    path.reverse()  # Reverse the path to show it from start to end

    # If the end node still has an infinite distance, no path was found
    if distances[end] == float("inf"):
        return distances[end], path

    # Return the total distance and the reconstructed path
    return distances[end], path

# ----------- Main execution block -----------

# Prompt the user to enter the CSV filename (including extension)
fileman = input("Enter the CSV filename (e.g., test123.csv): ").strip()
# Prompt the user to enter the start node
start = input("Enter the start node: ").strip()
# Prompt the user to enter the end node
end = input("Enter the end node: ").strip()

# Load the graph from the provided file
graph = import_graph(fileman)

# Run Dijkstra's algorithm to find the shortest distance and path
distance, path = dijkstra(graph, start, end)

# Output the result to the user
if distance == float("inf"):
    print(f"No path found from {start} to {end}.")  # Notify if no path was found
else:
    print(f"Shortest distance from {start} to {end}: {distance}")  # Print the shortest distance
    print(f"Path: {' -> '.join(path)}")  # Print the path as a sequence of nodes
