import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphCanvas:
    def __init__(self, root):
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_graph(self, graph, highlight_edges=None, highlight_nodes=None):
        self.ax.clear()
        # Increased k parameter for more spacing between nodes
        pos = nx.spring_layout(graph, k=5, iterations=50)

        edge_colors = ['red' if e in highlight_edges else 'gray' for e in graph.edges()] \
            if highlight_edges else 'gray'
        node_colors = ['yellow' if n in highlight_nodes else 'lightblue' for n in graph.nodes()] \
            if highlight_nodes else 'lightblue'

        nx.draw(graph, pos, with_labels=True, ax=self.ax,
                node_color=node_colors, edge_color=edge_colors,
                node_size=500, font_size=10,
                width=2.0,  # Increased edge width
                arrows=True,  # Show arrows for directed graphs
                arrowsize=20)  # Increased arrow size

        if nx.get_edge_attributes(graph, 'weight'):
            labels = nx.get_edge_attributes(graph, 'weight')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, ax=self.ax,
                                         font_size=8)

        self.canvas.draw()
