import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx


def load_graph_from_file(filename):
    """Load a graph from a text file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if len(lines) < 2:
            raise ValueError("Invalid file format! File too short.")

        # Process graph type
        graph_type = lines[0].strip().lower()
        graph_weighted = lines[1].strip().lower()

        directed = "directed" in graph_type
        weighted = "weighted" in graph_weighted

        # Create appropriate graph type
        graph = nx.DiGraph() if directed else nx.Graph()

        # Process edges
        for line in lines[2:]:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            if len(parts) == 2:  # Unweighted edge
                u, v = parts
                graph.add_edge(u, v)
            elif len(parts) == 3:  # Weighted edge
                u, v, w = parts
                graph.add_edge(u, v, weight=float(w))

        return graph

    except Exception as e:
        raise ValueError(f"Failed to load graph: {str(e)}")