# graph.py
import collections
import math

class Graph:
    def __init__(self):
        # adjacency_list[node] = list of (neighbor_node, edge_weight)
        self.adjacency_list = collections.defaultdict(list)
        # Stores (x, y) coordinates for each node
        self.node_coordinates = {}
    
    def load_map_data(self, filename):
        # Load the map from a CSV file
        # Each line has: start_id, start_x, start_y, end_id, end_x, end_y, weight
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue  # Skip comments or empty lines
                
                parts = line.strip().split(',')
                if len(parts) != 7:
                    continue  # Skip malformed lines
                
                start_id, start_x, start_y, end_id, end_x, end_y, weight = parts
                
                # Save node coordinates
                self.node_coordinates[start_id] = (float(start_x), float(start_y))
                self.node_coordinates[end_id] = (float(end_x), float(end_y))
                
                # Save edges in adjacency list (both directions for undirected graph)
                self.adjacency_list[start_id].append((end_id, float(weight)))
                self.adjacency_list[end_id].append((start_id, float(weight)))
    
    def find_nearest_vertex(self, point):
        # Given an (x, y) point, find the closest graph node
        if not self.node_coordinates:
            raise ValueError("No coordinates loaded")
        
        best_node = None
        best_distance = float('inf')
        
        # Iterate over all nodes and compute Euclidean distance
        for node_id, (node_x, node_y) in self.node_coordinates.items():
            distance = math.sqrt((point[0] - node_x)**2 + (point[1] - node_y)**2)
            if distance < best_distance:
                best_distance = distance
                best_node = node_id
        
        return best_node
    
    def get_bounds(self):
        # Return min_x, min_y, max_x, max_y of all nodes (used for Quadtree boundary)
        if not self.node_coordinates:
            return (0, 0, 7, 7)  # default fallback
        
        x_coords = [coord[0] for coord in self.node_coordinates.values()]
        y_coords = [coord[1] for coord in self.node_coordinates.values()]
        
        return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
